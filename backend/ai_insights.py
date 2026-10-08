"""Personalized resume insights.

Primary path is deterministic and rule-based so the product works with no
API key. If ANTHROPIC_API_KEY is set, insights are enhanced with Claude;
any API failure falls back to the rule-based version silently.
"""
from __future__ import annotations

import json
import os
import urllib.request

from matching_engine import MatchResult
from ats_scorer import ATSScore


def rule_based_insights(match: MatchResult, ats: ATSScore) -> list[str]:
    """Deterministic suggestions derived from the match + ATS analysis."""
    tips: list[str] = []

    missing = [
        (c.category, s)
        for c in match.categories
        for s in c.missing_skills
    ]
    if missing:
        top = ", ".join(f"{s} ({cat})" for cat, s in missing[:5])
        tips.append(
            f"Top missing skills the job asks for: {top}. "
            "Add the ones you genuinely have; learn the rest deliberately."
        )

    weak = [c for c in match.categories if c.score is not None and c.score < 0.5]
    if weak:
        cats = ", ".join(c.category for c in weak[:3])
        tips.append(
            f"Weakest areas vs. this job: {cats}. Move matching experience "
            "higher on the page so it is seen first."
        )

    for check in ats.checks:
        for fb in check.feedback[:2]:
            tips.append(f"ATS: {fb}")

    if match.overall_score >= 75:
        tips.append(
            "Strong match — tailor the top third of your resume to mirror the "
            "job post's exact phrasing for the final stretch."
        )
    elif match.overall_score < 40:
        tips.append(
            "Low match for this role. Either target roles closer to your stack "
            "or add a project that covers the biggest missing category."
        )
    return tips[:10]


def _claude_enhance(prompt: str) -> str | None:
    """Ask Claude for insight text; return None on any failure."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    try:
        body = json.dumps({
            "model": "claude-haiku-4-5-20251001",
            "max_tokens": 400,
            "messages": [{"role": "user", "content": prompt}],
        }).encode()
        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "content-type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        blocks = data.get("content", [])
        return "".join(b.get("text", "") for b in blocks if b.get("type") == "text") or None
    except Exception:
        return None


def generate_insights(
    resume_text: str, job_text: str, match: MatchResult, ats: ATSScore
) -> list[str]:
    """Rule-based insights, optionally enhanced with Claude."""
    tips = rule_based_insights(match, ats)
    prompt = (
        "You are a resume coach. Given this analysis, write 3 short, specific, "
        "actionable tips (one line each, no fluff):\n"
        f"Match score: {match.overall_score:.0f}/100. "
        f"ATS score: {ats.total:.0f}/100. "
        f"Current tips: {' | '.join(tips[:5])}"
    )
    enhanced = _claude_enhance(prompt)
    if enhanced:
        extra = [ln.strip("-• ").strip() for ln in enhanced.splitlines() if ln.strip()]
        return (tips + [e for e in extra if e])[:10]
    return tips
