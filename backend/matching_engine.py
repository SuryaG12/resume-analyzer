"""Weighted resume <-> job-description skill matching engine.

The engine extracts skills from free text using a curated taxonomy,
then scores the resume against the job description per category with
configurable weights. Categories with no skills in the job description
are excluded and the remaining weights are renormalized, so the final
score always reflects what the job actually asks for.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Skill:
    """A canonical skill plus the aliases that count as a mention."""

    name: str
    aliases: tuple[str, ...] = ()


# (canonical name, aliases...). Aliases let "k8s" count as Kubernetes, etc.
CATEGORIES: dict[str, dict] = {
    "Programming": {
        "weight": 0.22,
        "skills": [
            Skill("Python"),
            Skill("Java"),
            Skill("C++", ("c++",)),
            Skill("C", ("c lang",)),
            Skill("JavaScript", ("js",)),
            Skill("TypeScript", ("ts",)),
            Skill("Go", ("golang",)),
            Skill("Rust"),
            Skill("C#", ("c#", "csharp")),
            Skill("SQL"),
            Skill("HTML"),
            Skill("CSS"),
            Skill("Swift"),
            Skill("Kotlin"),
            Skill("R"),
            Skill("PHP"),
            Skill("Ruby"),
        ],
    },
    "Frameworks": {
        "weight": 0.18,
        "skills": [
            Skill("React", ("react.js", "reactjs")),
            Skill("Angular"),
            Skill("Vue", ("vue.js",)),
            Skill("Node.js", ("node", "nodejs")),
            Skill("Express", ("express.js",)),
            Skill("Django"),
            Skill("Flask"),
            Skill("FastAPI", ("fast api",)),
            Skill("Spring", ("spring boot",)),
            Skill(".NET", ("dotnet",)),
            Skill("Next.js", ("nextjs",)),
            Skill("Tailwind CSS", ("tailwind",)),
        ],
    },
    "Cloud & DevOps": {
        "weight": 0.16,
        "skills": [
            Skill("AWS", ("amazon web services",)),
            Skill("Azure", ("microsoft azure",)),
            Skill("GCP", ("google cloud", "google cloud platform")),
            Skill("Docker"),
            Skill("Kubernetes", ("k8s",)),
            Skill("CI/CD", ("cicd", "continuous integration")),
            Skill("Terraform"),
            Skill("Jenkins"),
            Skill("GitHub Actions", ("github actions",)),
            Skill("Linux"),
        ],
    },
    "Databases": {
        "weight": 0.12,
        "skills": [
            Skill("PostgreSQL", ("postgres",)),
            Skill("MySQL"),
            Skill("SQLite"),
            Skill("MongoDB", ("mongo",)),
            Skill("Redis"),
            Skill("Oracle DB", ("oracle",)),
            Skill("DynamoDB", ("dynamo db",)),
            Skill("Firebase"),
        ],
    },
    "Data & ML": {
        "weight": 0.12,
        "skills": [
            Skill("pandas"),
            Skill("NumPy", ("numpy",)),
            Skill("scikit-learn", ("sklearn",)),
            Skill("TensorFlow", ("tensorflow",)),
            Skill("PyTorch", ("pytorch",)),
            Skill("Machine Learning", ("ml",)),
            Skill("Deep Learning"),
            Skill("NLP", ("natural language processing",)),
            Skill("Data Analysis"),
            Skill("Statistics"),
            Skill("Matplotlib"),
            Skill("Jupyter"),
        ],
    },
    "Tools & Practices": {
        "weight": 0.10,
        "skills": [
            Skill("Git"),
            Skill("GitHub"),
            Skill("Agile", ("scrum",)),
            Skill("Testing", ("unit testing", "pytest", "jest")),
            Skill("REST APIs", ("rest", "restful")),
            Skill("GraphQL"),
            Skill("Jira"),
            Skill("Figma"),
            Skill("VS Code", ("vscode",)),
            Skill("Bash", ("shell scripting",)),
        ],
    },
    "Soft Skills": {
        "weight": 0.10,
        "skills": [
            Skill("Communication"),
            Skill("Teamwork", ("collaboration", "collaborative")),
            Skill("Leadership", ("led ", "leading")),
            Skill("Problem Solving", ("problem-solving",)),
            Skill("Mentoring", ("mentored", "mentor")),
            Skill("Time Management"),
        ],
    },
}


def _normalize(text: str) -> str:
    """Lowercase, strip sentence-terminal periods, collapse whitespace."""
    text = text.lower()
    # Remove periods that end a sentence ("PostgreSQL.") but keep interior
    # ones ("Node.js", "ASP.NET").
    text = re.sub(r"\.(?=\s|$)", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _mentioned(text: str, skill: Skill) -> bool:
    """True if the skill name or any alias appears as a standalone token."""
    candidates = (skill.name,) + skill.aliases
    for cand in candidates:
        pattern = r"(?<![\w+#.])" + re.escape(cand.lower()) + r"(?![\w+#.])"
        if re.search(pattern, text):
            return True
    return False


def extract_skills(text: str) -> dict[str, set[str]]:
    """Map each category to the set of canonical skills found in text."""
    norm = _normalize(text)
    found: dict[str, set[str]] = {}
    for category, spec in CATEGORIES.items():
        hits = {s.name for s in spec["skills"] if _mentioned(norm, s)}
        found[category] = hits
    return found


@dataclass
class CategoryResult:
    category: str
    weight: float
    job_skills: list[str] = field(default_factory=list)
    matched_skills: list[str] = field(default_factory=list)
    missing_skills: list[str] = field(default_factory=list)
    score: float | None = None  # None => category not required by the job


@dataclass
class MatchResult:
    overall_score: float  # 0-100
    categories: list[CategoryResult]
    total_job_skills: int
    total_matched: int

    def to_dict(self) -> dict:
        return {
            "overall_score": round(self.overall_score, 1),
            "total_job_skills": self.total_job_skills,
            "total_matched": self.total_matched,
            "categories": [
                {
                    "category": c.category,
                    "weight": c.weight,
                    "score": None if c.score is None else round(c.score * 100, 1),
                    "job_skills": sorted(c.job_skills),
                    "matched_skills": sorted(c.matched_skills),
                    "missing_skills": sorted(c.missing_skills),
                }
                for c in self.categories
            ],
        }


def match_resume_to_job(resume_text: str, job_text: str) -> MatchResult:
    """Score a resume against a job description.

    Returns per-category scores plus an overall 0-100 score computed as
    the weight-renormalized average over categories the job requires.
    """
    resume_skills = extract_skills(resume_text or "")
    job_skills = extract_skills(job_text or "")

    categories: list[CategoryResult] = []
    weighted_sum = 0.0
    weight_total = 0.0
    for category, spec in CATEGORIES.items():
        job = job_skills[category]
        if not job:
            categories.append(
                CategoryResult(category=category, weight=spec["weight"])
            )
            continue
        matched = job & resume_skills[category]
        score = len(matched) / len(job)
        categories.append(
            CategoryResult(
                category=category,
                weight=spec["weight"],
                job_skills=sorted(job),
                matched_skills=sorted(matched),
                missing_skills=sorted(job - matched),
                score=score,
            )
        )
        weighted_sum += spec["weight"] * score
        weight_total += spec["weight"]

    overall = (weighted_sum / weight_total * 100) if weight_total else 0.0
    return MatchResult(
        overall_score=overall,
        categories=categories,
        total_job_skills=sum(len(job_skills[c]) for c in CATEGORIES),
        total_matched=sum(len(c.matched_skills) for c in categories),
    )
