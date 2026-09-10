# Contributing to ResumeIQ

Thank you for your interest in contributing! This document outlines the process for contributing to ResumeIQ.

## Code of Conduct

Be respectful, inclusive, and collaborative. No harassment or discrimination.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/resume-analyzer.git`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Follow the setup instructions in `SETUP.md`

## Development Guidelines

### Code Style

**Python (Backend)**
- PEP 8 style guide
- Type hints where possible
- Docstrings for all functions
- Lines max 100 characters

**JavaScript (Frontend)**
- Use ES6+ syntax
- Meaningful variable names
- Comments for complex logic
- Functional components (React hooks)

### Commits

Use clear, descriptive commit messages:
```
feat: add skill extraction
fix: resolve ATS scoring bug
docs: update README
test: add unit tests for matching engine
refactor: simplify section detection
```

### Testing

**Backend**
```bash
cd backend
pytest tests/ -v
```

**Frontend**
```bash
cd frontend
npm test
```

All new features must include tests. Aim for >80% coverage.

## Pull Request Process

1. Update `README.md` with any new information
2. Ensure all tests pass: `pytest tests/ -v` (backend)
3. Ensure code follows style guidelines
4. Write a clear PR description
5. Link related issues with "Closes #123"
6. Request review from maintainers

Example PR template:
```markdown
## Description
What does this PR do?

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Tests pass
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Commit messages are clear
```

## Roadmap

- [ ] Phase 1: ✅ Custom matching engine + ATS scorer
- [ ] Phase 2: PDF/DOCX text extraction
- [ ] Phase 3: NLP improvements (spaCy)
- [ ] Phase 4: Multi-job comparison
- [ ] Phase 5: Resume revision tracking
- [ ] Phase 6: Public dashboard + analytics
- [ ] Phase 7: Mobile app (React Native)

## Issues & Feature Requests

### Found a Bug?
1. Check if it's already reported
2. Include steps to reproduce
3. Include expected vs actual behavior
4. Include your environment (OS, Python version, etc.)

### Want a Feature?
1. Describe the feature and use case
2. Explain how it benefits users
3. Include any relevant examples

## Questions?

- Open a discussion on GitHub
- Create an issue with [QUESTION] label
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🚀
