"""Tests for the ATS scorer."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ats_scorer import score_ats

STRONG_RESUME = """\
Jane Doe
jane.doe@example.com | (555) 123-4567 | linkedin.com/in/janedoe | github.com/janedoe

Summary
Software engineer with 3 years of experience building web applications.

Experience
- Built a REST API serving 10k daily users, reducing latency by 40%.
- Led a team of 4 engineers to ship a payments dashboard used by 200+ merchants.
- Automated deployment pipelines, cutting release time from 2 hours to 15 minutes.

Education
B.S. Computer Science, Example University, 2022.

Skills
Python, FastAPI, React, PostgreSQL, Docker, AWS, Git.
"""

WEAK_RESUME = "hi im jane\ni like computers\n"


def test_strong_resume_scores_high():
    result = score_ats(STRONG_RESUME)
    assert result.total >= 70, f"expected >= 70, got {result.total}"


def test_weak_resume_scores_low():
    result = score_ats(WEAK_RESUME)
    assert result.total < 40, f"expected < 40, got {result.total}"


def test_empty_resume_scores_zero():
    assert score_ats("").total == 0.0
    assert score_ats("   ").total == 0.0


def test_feedback_is_actionable():
    result = score_ats(WEAK_RESUME)
    all_feedback = [fb for c in result.checks for fb in c.feedback]
    assert len(all_feedback) > 0
    assert any("email" in fb.lower() for fb in all_feedback)


def test_score_bounded():
    assert 0 <= score_ats(STRONG_RESUME).total <= 100
