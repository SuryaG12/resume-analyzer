# ResumeQue — AI Resume ↔ Job Matching Engine

A full-stack resume analysis tool that scores your resume against job descriptions using a custom weighted matching algorithm, ATS simulation, and AI-generated insights.

![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-beta-yellow)

## 🎯 What It Does

**Resume ↔ Job Matching**
- Extracts skills from both resume and job description
- Compares across 7 skill categories with weighted scoring
- Shows match percentage for each category
- Highlights matched and missing skills

**ATS Simulation** 
- Scores resume for ATS compatibility (0–100)
- Analyzes keyword density, section structure, formatting
- Detects contact info, quantified achievements, resume length
- Flags potential ATS rejection points

**AI-Generated Insights**
- Personalized resume improvement suggestions
- Before/after bullet point examples
- Strategic advice based on matching results
- Missing skill recommendations

## 🏗️ Tech Stack

**Frontend**
- React (Vite)
- TypeScript
- Tailwind CSS (custom theme)

**Backend**
- Python 3.9+
- FastAPI
- spaCy (future: NLP enhancements)

**AI Layer**
- Claude API (Anthropic)

**Database**
- PostgreSQL (production)
- SQLite (local development)

**Deployment**
- Vercel (frontend)
- Render or Railway (backend)

## 📦 Project Structure

```
resume-analyzer/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── matching_engine.py   # Custom matching algorithm
│   ├── ats_scorer.py        # ATS scoring engine
│   ├── ai_insights.py       # AI insight generation
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── resume-analyzer.jsx  # React component
│   └── src/
└── README.md
```

## ⚡ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- OpenAI API key (for AI insights)

### Local Development

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/resume-analyzer.git
cd resume-analyzer
```

**2. Backend setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

pip install -r requirements.txt
python main.py
```

Server runs on `http://localhost:8000`

**3. Frontend setup**
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🧠 Matching Engine (The Core)

The custom matching engine is what makes this project stand out.

### How It Works

1. **Skill Extraction** — Extract skills from resume and job description using regex + keyword matching
2. **Categorization** — Organize skills into 7 categories (Programming, Frameworks, Cloud, Databases, Data/ML, Tools, Soft Skills)
3. **Weighted Scoring** — Each category has a weight based on importance:
   - Programming: 22%
   - Frameworks: 18%
   - Cloud & DevOps: 16%
   - Databases: 12%
   - Data & ML: 12%
   - Tools & Practices: 10%
   - Soft Skills: 10%
4. **Match Calculation** — For each category, calculate (matched skills / required skills) × weight
5. **Aggregate Score** — Sum weighted category scores → 0–100 match percentage

### ATS Simulation

ATS scoring is based on real resume scanning systems:
- **Keywords (30 pts)** — How many job-description skills appear in resume
- **Structure (25 pts)** — Standard section detection (Experience, Education, Skills, Projects, etc.)
- **Achievements (20 pts)** — Count of quantified accomplishments (numbers, percentages, metrics)
- **Length (15 pts)** — Word count analysis (ideal: 300–750 words)
- **Contact Info (10 pts)** — Email, phone, LinkedIn presence

Total: 0–100 ATS score

## 📊 Data

### Skill Database
Located in `backend/matching_engine.py`, the `SKILL_DB` dictionary contains:
- 100+ technology terms
- 7 categories with weighted importance
- Regex patterns for skill detection

Add new skills by editing the dictionary:
```python
SKILL_DB = {
    "programming": {
        "label": "Programming",
        "weight": 0.22,
        "terms": ["python", "javascript", ...]
    },
    ...
}
```

## 🚀 Roadmap

- [ ] Phase 1: ✅ Custom matching engine + ATS scorer
- [ ] Phase 2: PDF/DOCX text extraction (backend)
- [ ] Phase 3: Section detection improvements (spaCy NLP)
- [ ] Phase 4: Multi-job comparison (rank 5 jobs)
- [ ] Phase 5: Resume revision tracking
- [ ] Phase 6: Public dashboard + anonymized analytics
- [ ] Phase 7: Mobile app (React Native)

## 🔧 API Endpoints

### `POST /analyze`
```json
{
  "resume": "...",
  "job_description": "...",
  "use_ai": true
}
```

**Response:**
```json
{
  "match": {
    "overall": 84,
    "categories": { "programming": 91, ... }
  },
  "ats": {
    "total": 78,
    "breakdown": { "keywords": 30, ... }
  },
  "ai_insights": {
    "topStrengths": [...],
    "missingSkills": [...],
    "bulletImprovements": [...]
  }
}
```

## 📈 Performance

- Matching engine: <100ms
- ATS scoring: <50ms
- AI insights: 2–4 seconds (depends on API)
- Total end-to-end: <5 seconds

## 🧪 Testing

Run the test suite:
```bash
cd backend
pytest tests/
```

Example test:
```bash
pytest tests/test_matching_engine.py -v
```

## 📝 License

MIT License — see `LICENSE` file for details

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Questions? Reach out or open an issue on GitHub.

---

**Built with ⚡ by SG**

Built and deployed an NLP-based resume-to-job matching platform using React, FastAPI, PostgreSQL, semantic embeddings, and a custom weighted scoring algorithm.
