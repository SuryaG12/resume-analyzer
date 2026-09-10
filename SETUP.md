# Local Development Setup

## Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- Git
- Anthropic API key (for AI insights)

## Backend Setup (Python)

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Run Tests

```bash
pytest tests/ -v
```

### 5. Start the Backend Server

```bash
python main.py
```

The backend will run on `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

## Frontend Setup (React)

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

## Testing the Full Stack

### 1. Make sure both servers are running
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:5173`

### 2. Open the app
Navigate to `http://localhost:5173` in your browser

### 3. Try the example
Click "Try with example →" button to load sample resume and job description

### 4. Run analysis
Click "Run Analysis" to see the matching engine and ATS scorer in action

## Backend API Usage

### Analyze a Resume

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "resume": "Python developer with 5 years experience",
    "job_description": "Looking for a Python engineer",
    "use_ai": true
  }'
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Running Unit Tests

```bash
cd backend
pytest tests/ -v
```

Test coverage:
- `test_matching_engine.py` - Skill extraction, section detection, matching algorithm
- `test_ats_scorer.py` - ATS scoring, contact detection, quantified achievements

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (should be 3.9+)
- Check all dependencies installed: `pip install -r requirements.txt`
- Check port 8000 is available: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (should be 16+)
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

### API calls failing
- Make sure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Check browser console for specific error messages

### AI insights not working
- Set `ANTHROPIC_API_KEY` in `.env` file
- Test API key with: `curl https://api.anthropic.com/v1/models -H "Authorization: Bearer $ANTHROPIC_API_KEY"`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes to backend or frontend
3. Run tests: `pytest tests/ -v` (backend) or `npm test` (frontend)
4. Commit changes: `git commit -m "feat: description"`
5. Push to GitHub: `git push origin feature/your-feature`
6. Open a Pull Request

## Environment Variables Reference

### Backend (.env)
```
ANTHROPIC_API_KEY=sk-ant-...          # Anthropic API key for AI insights
FASTAPI_ENV=development                # Environment (development/production)
FASTAPI_DEBUG=true                     # Enable debug mode
DATABASE_URL=sqlite:///./test.db       # Database connection string
ALLOWED_ORIGINS=http://localhost:5173  # CORS allowed origins
HOST=0.0.0.0                           # Server host
PORT=8000                              # Server port
```

## Next Steps

- Add PDF/DOCX text extraction (Phase 2)
- Improve NLP with spaCy (Phase 3)
- Build multi-job comparison (Phase 4)
- Deploy to production
