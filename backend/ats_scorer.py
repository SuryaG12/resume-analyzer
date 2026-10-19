"""Heuristic ATS (applicant tracking system) compatibility scorer.

Scores a resume 0-100 across checks that mirror what real ATS parsers
look at: contact info, standard section headers, quantified achievements,
length, action verbs, and formatting red flags. Every check returns its
points plus human-readable feedback, so the score is explainable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class CheckResult:
    name: str
    max_points: float
    points: float
    feedback: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "max_points": self.max_points,
            "points": round(self.points, 1),
            "feedback": self.feedback,
        }


@dataclass
class ATSScore:
    total: float  # 0-100
    checks: list[CheckResult]

    def to_dict(self) -> dict:
        return {
            "total": round(self.total, 1),
            "explanation": explain_ats_score(self),
            "checks": [c.to_dict() for c in self.checks],
        }


def explain_ats_score(result: ATSScore) -> str:
    """Plain-English explanation of what drove an ATS score.

    Built entirely from the check results, so the words always match
    the number: the verdict band comes from the total, the strengths
    from full-marks checks, and the drags from the checks with the
    most missed points (with their own actionable feedback as the fix).
    """
    total = round(result.total, 1)
    if total == 0:
        return (
            "There's no score here yet — the resume text looks empty or "
            "unscannable. Paste your full resume text to get a score and a "
            "breakdown of what's helping or hurting it."
        )
    if total >= 85:
        verdict = (f"Scores {total:g}/100 — excellent. "
                   "This resume should sail through most ATS parsers.")
    elif total >= 70:
        verdict = (f"Scores {total:g}/100 — strong and largely ATS-friendly, "
                   "with a few fixable gaps.")
    elif total >= 40:
        verdict = (f"Scores {total:g}/100 — needs work. "
                   "Several fixable issues are dragging it down.")
    else:
        verdict = (f"Scores {total:g}/100 — weak. "
                   "An ATS parser would likely filter this out before a human sees it.")

    full_marks = [c for c in result.checks if c.max_points and c.points >= c.max_points]
    gaps = sorted(
        (c for c in result.checks if c.max_points and c.points < c.max_points),
        key=lambda c: (c.max_points - c.points),
        reverse=True,
    )
    parts = [verdict]
    if full_marks:
        names = " and ".join(c.name.lower() for c in full_marks[:2])
        parts.append(f"It's carried by {names} — full marks there.")
    if gaps:
        top = gaps[0]
        fix = top.feedback[0] if top.feedback else "give this section another pass."
        if len(gaps) > 1 and gaps[1].feedback:
            second = gaps[1]
            parts.append(
                f"The biggest drag is {top.name.lower()} "
                f"({top.points:g}/{top.max_points:g} points): {fix} "
                f"Next: {second.name.lower()} — {second.feedback[0]}"
            )
        else:
            parts.append(
                f"The biggest drag is {top.name.lower()} "
                f"({top.points:g}/{top.max_points:g} points): {fix}"
            )
    else:
        parts.append("Nothing major is holding it back.")
    return " ".join(parts)


EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_RE = re.compile(r"(\+?1[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}")
URL_RE = re.compile(r"(linkedin\.com|github\.com)[/\w.\-@]*", re.IGNORECASE)

SECTION_HEADERS = {
    "experience": ("experience", "work history", "employment"),
    "education": ("education", "academic background",),
    "skills": ("skills", "technical skills", "core competencies"),
    "projects": ("projects", "personal projects"),
    "summary": ("summary", "objective", "profile"),
}

ACTION_VERBS = (
    "built", "developed", "designed", "implemented", "led", "created",
    "launched", "improved", "increased", "reduced", "automated", "architected",
    "deployed", "optimized", "managed", "delivered", "engineered", "founded",
    "analyzed", "collaborated", "spearheaded", "migrated", "refactored",
    "shipped", "owned", "drove",
)

QUANT_RE = re.compile(r"(\d+\s?%|\$\s?[\d,]+|\d+\s?(x|times)|\d{2,}\+?)")


def _lines(text: str) -> list[str]:
    return [ln.strip() for ln in text.splitlines() if ln.strip()]


def check_contact_info(text: str) -> CheckResult:
    points, feedback = 0.0, []
    if EMAIL_RE.search(text):
        points += 8
    else:
        feedback.append("No email address detected — add one near the top.")
    if PHONE_RE.search(text):
        points += 6
    else:
        feedback.append("No phone number detected.")
    if URL_RE.search(text):
        points += 6
    else:
        feedback.append("Add a LinkedIn or GitHub link — parsers and recruiters look for it.")
    return CheckResult("Contact information", 20, points, feedback)


def check_sections(text: str) -> CheckResult:
    lowered = text.lower()
    found = [name for name, aliases in SECTION_HEADERS.items()
             if any(a in lowered for a in aliases)]
    points = min(20.0, len(found) * 5)
    feedback = []
    for must in ("experience", "education", "skills"):
        if must not in found:
            feedback.append(f"Missing a clear '{must}' section header.")
    return CheckResult("Section headers", 20, points, feedback)


def check_quantified_achievements(text: str) -> CheckResult:
    hits = QUANT_RE.findall(text)
    points = min(15.0, len(hits) * 3)
    feedback = []
    if len(hits) < 3:
        feedback.append(
            "Few quantified achievements — add numbers (%, $, users, latency) "
            "to prove impact."
        )
    return CheckResult("Quantified achievements", 15, points, feedback)


def check_length(text: str) -> CheckResult:
    words = len(text.split())
    if 300 <= words <= 900:
        points, feedback = 10.0, []
    elif words < 300:
        points, feedback = 5.0, [f"Only ~{words} words — a bit thin; aim for 300+."]
    else:
        points, feedback = 6.0, [f"~{words} words — long; trim toward one page (~900 words max)."]
    return CheckResult("Length", 10, points, feedback)


def check_action_verbs(text: str) -> CheckResult:
    bullets = [ln for ln in _lines(text) if ln[:2] in ("- ", "* ", "• ")]
    if not bullets:
        bullets = _lines(text)
    strong = sum(1 for b in bullets if b.lstrip("-*• ").split(" ")[0].lower() in ACTION_VERBS)
    ratio = strong / max(1, len(bullets))
    points = min(10.0, ratio * 12)
    feedback = []
    if ratio < 0.4:
        feedback.append("Start more bullets with strong action verbs (built, led, shipped…).")
    return CheckResult("Action verbs", 10, points, feedback)


def check_formatting(text: str) -> CheckResult:
    points, feedback = 10.0, []
    if len(re.findall(r"[^\x00-\x7F]", text)) > 15:
        points -= 3
        feedback.append("Heavy use of special characters can confuse older ATS parsers.")
    long_lines = sum(1 for ln in _lines(text) if len(ln) > 220)
    if long_lines > 3:
        points -= 3
        feedback.append("Several very long lines — break dense paragraphs into bullets.")
    if re.search(r"\b(table|columns?)\b", text.lower()):
        points -= 2
        feedback.append("Avoid tables/columns layouts; single-column text parses best.")
    return CheckResult("ATS-friendly formatting", 10, max(0.0, points), feedback)


def score_ats(resume_text: str) -> ATSScore:
    """Score resume text for ATS compatibility (0-100, explainable)."""
    text = resume_text or ""
    checks = [
        check_contact_info(text),
        check_sections(text),
        check_quantified_achievements(text),
        check_length(text),
        check_action_verbs(text),
        check_formatting(text),
    ]
    total = sum(c.points for c in checks)
    if not text.strip():
        return ATSScore(total=0.0, checks=checks)
    # Keyword relevance (15): overlap of resume skills with common tech terms.
    from matching_engine import extract_skills  # local import: keeps module standalone

    found = sum(len(s) for s in extract_skills(text).values())
    kw_points = min(15.0, found * 1.5)
    kw_feedback = []
    if found < 8:
        kw_feedback.append("Few recognizable skills keywords — mirror the job post's terminology.")
    checks.append(CheckResult("Keyword relevance", 15, kw_points, kw_feedback))
    total += kw_points
    return ATSScore(total=min(100.0, total), checks=checks)
