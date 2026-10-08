# Local Development Setup

## Prerequisites

- Python 3.9 or higher
- Git
- (Optional) Anthropic API key for Claude-enhanced AI insights

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/SuryaG12/resume-analyzer.git
cd resume-analyzer
```

### 2. Create a virtual environment

```bash
cd backend
python -m venv venv

# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the tests

```bash
pytest tests/ -v
```

All 11 tests should pass.

### 5. Start the app

```bash
python app.py
```

Open `http://localhost:8000` in your browser. The single-page frontend is
served directly by the backend — no separate frontend server or build step.

API docs: `http://localhost:8000/docs`

## AI insights (optional)

For Claude-enhanced insights:

```bash
export ANTHROPIC_API_KEY=sk-ant-...   # macOS/Linux
# set ANTHROPIC_API_KEY=sk-ant-...    # Windows

python app.py
```

Without the key, the app uses its built-in rule-based insight engine.
