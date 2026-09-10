# Push This Project to GitHub

## Step 1: Create a GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `resume-analyzer`
3. Description: `AI-powered resume ↔ job matching engine with custom scoring algorithm`
4. Choose: **Public** (for portfolio)
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Add Remote and Push

In your terminal, in the resume-analyzer directory:

```bash
# Add the GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/resume-analyzer.git

# Rename master to main (GitHub default)
git branch -M main

# Push all commits to GitHub
git push -u origin main
```

## Step 3: Verify on GitHub

1. Go to your repository: `https://github.com/USERNAME/resume-analyzer`
2. Check that all files are there
3. Check the commit history

## Step 4: Add Topics (for discoverability)

On GitHub repo page → "About" → Add topics:
- `resume-analyzer`
- `job-matching`
- `python`
- `react`
- `fastapi`
- `matching-engine`
- `ats-score`
- `portfolio-project`

## Step 5: Add a Meaningful README Badge

Edit `README.md` - add at the top:

```markdown
# ResumeIQ — AI Resume ↔ Job Matching Engine

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Node 16+](https://img.shields.io/badge/node-16%2B-green)](https://nodejs.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-yellow)]()

An AI-powered resume analysis tool that scores your resume against job descriptions using a custom weighted matching algorithm, ATS simulation, and AI-generated insights.

[Try the Demo](#) | [Read the Docs](SETUP.md) | [Contribute](CONTRIBUTING.md)
```

## Step 6 (Optional): Set Up GitHub Actions for CI/CD

Create `.github/workflows/tests.yml`:

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        pytest tests/ -v
```

## Step 7 (Optional): Deploy Frontend to Vercel

### Free hosting for React frontend

1. Go to [vercel.com](https://vercel.com) and sign up with GitHub
2. Click "New Project"
3. Import your `resume-analyzer` repository
4. Framework: **Vite**
5. Root Directory: `frontend`
6. Environment: (leave blank for now)
7. Deploy!

Your frontend will be live at: `https://resume-analyzer-git-main-USERNAME.vercel.app`

## Step 8 (Optional): Deploy Backend to Render

### Free hosting for Python API

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click "New +"
3. Select "Web Service"
4. Connect your GitHub repo
5. Settings:
   - Name: `resume-analyzer-api`
   - Environment: `Python 3`
   - Build command: `pip install -r backend/requirements.txt`
   - Start command: `cd backend && python main.py`
   - Root directory: `.`
6. Add environment variable:
   - `ANTHROPIC_API_KEY` = your API key
7. Deploy!

Your API will be at: `https://resume-analyzer-api-XXXX.onrender.com`

Then update `frontend/vite.config.js`:
```js
proxy: {
  '/api': {
    target: 'https://resume-analyzer-api-XXXX.onrender.com',
    // ...
  }
}
```

## Step 9: Update README with Live Links

Edit `README.md` - add after installation:

```markdown
## 🚀 Live Demo

- **Frontend**: https://resume-analyzer-git-main-USERNAME.vercel.app
- **API Docs**: https://resume-analyzer-api-XXXX.onrender.com/docs

Try the example or upload your own resume!
```

## Troubleshooting

### "fatal: refusing to merge unrelated histories"

```bash
git pull origin main --allow-unrelated-histories
```

### "Permission denied (publickey)"

Set up SSH keys:
```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
# Add the public key to GitHub Settings → SSH Keys
```

Then use SSH URL:
```bash
git remote set-url origin git@github.com:USERNAME/resume-analyzer.git
```

### "origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/resume-analyzer.git
```

## Done! 🎉

Your project is now on GitHub! Share the link:

```
https://github.com/USERNAME/resume-analyzer
```

This is a solid portfolio project for your UW Bothell application.
