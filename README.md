# ResumeQue — AI Resume ↔ Job Matching Engine

A resume analysis tool that scores your resume against job descriptions using a
custom weighted matching algorithm, ATS simulation, and AI-generated insights.

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-working-green)
![Tests](https://img.shields.io/badge/tests-11%20passing-green)

## 🎯 What It Does

**Resume ↔ Job Matching**
- Extracts skills from both resume and job description
- Compares across 7 skill categories with weighted scoring
- Shows match percentage for each category
- Highlights matched and missing skills

**ATS Simulation**
- Scores resume for ATS compatibility (0–100)
- Analyzes contact info, section structure, quantified achievements
- Detects formatting red flags that trip up parsers

**AI-Generated Insights**
- Personalized resume improvement suggestions
- Works out of the box with rule-based insights — no API key needed
- Optionally enhanced with Claude when `ANTHROPIC_API_KEY` is set

## 🏗️ Tech Stack

- **Backend:** Python 3.9+, FastAPI
- **Frontend:** Single-page app (HTML/CSS/vanilla JS), served by the backend — no build step
- **AI Layer:** Rule-based insights, optional Claude API enhancement
- **Testing:** pytest (11 tests)

## 📦 Project Structure

```
resume-analyzer/
├── backend/
│   ├── app.py               # FastAPI server + API routes
│   ├── matching_engine.py   # Weighted skill-matching algorithm
│   ├── ats_scorer.py        # ATS compatibility scorer
│   ├── ai_insights.py       # Insight generation (rule-based + optional Claude)
│   ├── requirements.txt
│   └── tests/               # pytest suite
├── frontend/
│   └── index.html           # Single-page UI
└── README.md
```

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Git

### Run it

```bash
git clone https://github.com/SuryaG12/resume-analyzer.git
cd resume-analyzer/backend

python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate          # Windows

pip install -r requirements.txt
python app.py
```

Open `http://localhost:8000` — paste your resume and a job description, hit
**Analyze match**.

### Run the tests

```bash
cd backend
pytest tests/ -v
```

### API

| Method | Endpoint       | Description                              |
|--------|---------------|------------------------------------------|
| GET    | `/api/health` | Health check                             |
| POST   | `/api/analyze` | `{resume_text, job_text}` → match + ATS + insights |

Interactive docs at `http://localhost:8000/docs` (FastAPI auto-generates them).

### AI insights (optional)

Set `ANTHROPIC_API_KEY` to have Claude enhance the rule-based insights.
Without it, everything still works — the rule-based engine covers it.

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python app.py
```

## 🧠 Matching Engine (The Core)

1. **Skill Extraction** — Skills are detected via a curated taxonomy with
   aliases (`k8s` → Kubernetes, `postgres` → PostgreSQL), matched on token
   boundaries so "Java" never matches "JavaScript".
2. **Categorization** — Skills roll up into 7 categories (Programming,
   Frameworks, Cloud & DevOps, Databases, Data & ML, Tools & Practices,
   Soft Skills).
3. **Weighted Scoring** — Each category carries a weight (Programming 22%,
   Frameworks 18%, Cloud & DevOps 16%, Databases 12%, Data & ML 12%,
   Tools & Practices 10%, Soft Skills 10%).
4. **Renormalization** — Categories the job doesn't mention are excluded and
   remaining weights are renormalized, so the score reflects what the job
   actually asks for.

## 📄 License

MIT — see [LICENSE](LICENSE).
