"""Tests for the weighted matching engine."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from matching_engine import extract_skills, match_resume_to_job


def test_extract_skills_finds_aliases():
    found = extract_skills("I use k8s, React.js and postgres daily.")
    assert "Kubernetes" in found["Cloud & DevOps"]
    assert "React" in found["Frameworks"]
    assert "PostgreSQL" in found["Databases"]


def test_perfect_match_scores_100():
    job = "We need Python, React, AWS and PostgreSQL experience."
    resume = "Python developer with React, AWS and PostgreSQL. " * 5
    result = match_resume_to_job(resume, job)
    assert result.overall_score == 100.0
    assert result.total_matched == result.total_job_skills


def test_empty_resume_scores_zero():
    job = "We need Python and React."
    result = match_resume_to_job("", job)
    assert result.overall_score == 0.0


def test_irrelevant_categories_are_excluded():
    # Job mentions only programming: other categories must not dilute the score.
    job = "Python required."
    resume = "Python expert."
    result = match_resume_to_job(resume, job)
    assert result.overall_score == 100.0
    prog = next(c for c in result.categories if c.category == "Programming")
    assert prog.score == 1.0
    cloud = next(c for c in result.categories if c.category == "Cloud & DevOps")
    assert cloud.score is None


def test_missing_skills_reported():
    job = "Need Python, Docker and Kubernetes."
    resume = "Python developer."
    result = match_resume_to_job(resume, job)
    cloud = next(c for c in result.categories if c.category == "Cloud & DevOps")
    assert set(cloud.missing_skills) == {"Docker", "Kubernetes"}
    assert result.overall_score < 100.0
    assert result.overall_score > 0.0


def test_weights_sum_to_one():
    from matching_engine import CATEGORIES

    total = sum(spec["weight"] for spec in CATEGORIES.values())
    assert abs(total - 1.0) < 1e-9
