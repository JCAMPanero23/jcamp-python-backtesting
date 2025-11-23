# Contributing to JCAMP Python Backtesting Engine

Thank you for considering contributing to the JCAMP Python Backtesting Engine! This document provides guidelines for contributing to the project.

---

## 📋 **Table of Contents**

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Feature Requests](#feature-requests)

---

## 📜 **Code of Conduct**

This project adheres to a code of conduct that all contributors are expected to follow:

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Acknowledge different perspectives
- Show empathy towards others

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.10 or higher
- Git
- Basic understanding of forex trading concepts
- Familiarity with pandas and NumPy

### **First Time Contributors**

Look for issues labeled with:
- `good first issue` - Great for newcomers
- `help wanted` - Community input needed
- `documentation` - Improve docs

---

## 🛠️ **Development Setup**

### **1. Fork and Clone**

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/jcamp-python-backtesting.git
cd jcamp-python-backtesting
```

### **2. Create Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### **4. Verify Setup**

```bash
# Run tests to ensure everything works
pytest tests/

# Run linting
flake8 src/
black --check src/
```

---

## 🔨 **Making Changes**

### **1. Create a Branch**

```bash
# Create feature branch from main
git checkout -b feature/your-feature-name

# Or for bug fixes:
git checkout -b fix/bug-description
```

### **Branch Naming Convention:**

- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications
- `perf/` - Performance improvements

### **2. Make Your Changes**

- Keep changes focused and atomic
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

### **3. Commit Messages**

Follow conventional commit format:

```
type(scope): Brief description

Detailed explanation if needed

Fixes #123
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting
- `refactor:` - Code restructuring
- `test:` - Test changes
- `perf:` - Performance improvements
- `chore:` - Maintenance tasks

**Example:**
```
feat(optimizer): Add walk-forward analysis

Implements walk-forward optimization with configurable
periods and metrics. Includes validation against
overfitting.

Closes #45
```

---

## 🧪 **Testing**

### **Running Tests**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_indicators.py

# Run with coverage
pytest --cov=src tests/

# Run only fast tests
pytest -m "not slow"
```

### **Writing Tests**

- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Name test functions as `test_*`
- Use fixtures for setup/teardown
- Mock external dependencies

**Example:**

```python
# tests/test_indicators.py
import pytest
from src.core.indicators import calculate_ema

def test_ema_calculation():
    """Test EMA calculation matches expected values."""
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    period = 3
    
    result = calculate_ema(data, period)
    
    assert len(result) == len(data)
    assert result[-1] > 0  # EMA should be positive
    # Add more specific assertions
```

### **Test Coverage Requirements**

- Aim for >80% code coverage
- Critical functions should have >95% coverage
- All new features must include tests

---

## 🎨 **Code Style**

### **Python Style Guide**

We follow PEP 8 with some modifications:

- **Line length:** 100 characters (not 79)
- **Quotes:** Double quotes for strings
- **Imports:** Organized with isort
- **Formatting:** Black code formatter
- **Type hints:** Required for public functions

### **Auto-formatting**

```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Run both (recommended)
black src/ tests/ && isort src/ tests/
```

### **Type Hints**

```python
# Good - with type hints
def calculate_r_multiple(
    entry_price: float,
    exit_price: float,
    stop_loss: float
) -> float:
    """Calculate R-multiple for a trade."""
    risk = abs(entry_price - stop_loss)
    profit = exit_price - entry_price
    return profit / risk if risk > 0 else 0.0

# Bad - no type hints
def calculate_r_multiple(entry_price, exit_price, stop_loss):
    risk = abs(entry_price - stop_loss)
    profit = exit_price - entry_price
    return profit / risk if risk > 0 else 0.0
```

### **Docstrings**

Use Google-style docstrings:

```python
def run_backtest(
    symbol: str,
    start_date: str,
    end_date: str,
    strategy: str = "both"
) -> BacktestResults:
    """
    Run a backtest for the specified symbol and period.
    
    Args:
        symbol: Trading pair symbol (e.g., "EURUSD")
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        strategy: Strategy to test ("trend_rider", "range_rider", "both")
        
    Returns:
        BacktestResults object containing performance metrics
        
    Raises:
        ValueError: If dates are invalid or symbol not found
        
    Examples:
        >>> results = run_backtest("EURUSD", "2024-01-01", "2024-12-31")
        >>> print(f"Total R: {results.total_r:.2f}")
    """
    pass
```

---

## 📤 **Submitting Changes**

### **1. Update Your Branch**

```bash
# Fetch latest changes from main
git fetch origin main

# Rebase your branch
git rebase origin/main

# Resolve any conflicts
```

### **2. Push Changes**

```bash
# Push to your fork
git push origin feature/your-feature-name
```

### **3. Create Pull Request**

1. Go to GitHub repository
2. Click "Pull Request"
3. Select your branch
4. Fill out PR template:
   - **Title:** Clear, descriptive summary
   - **Description:** What changed and why
   - **Testing:** How you tested changes
   - **Screenshots:** If UI changes
   - **Related Issues:** Link to issues

### **4. PR Checklist**

Before submitting, ensure:

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted (`black`, `isort`)
- [ ] Linting passes (`flake8`)
- [ ] Type checking passes (`mypy`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] All commits are meaningful
- [ ] Branch is up to date with main

### **5. Code Review Process**

- Maintainers will review your PR
- Address feedback promptly
- Be open to suggestions
- Once approved, PR will be merged

---

## 🐛 **Reporting Bugs**

### **Before Reporting**

1. Check existing issues
2. Verify bug on latest version
3. Try to reproduce consistently
4. Gather relevant information

### **Bug Report Template**

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.10.5]
- Package version: [e.g., 1.0.0]

## Additional Context
- Error messages
- Screenshots
- Relevant logs
```

---

## 💡 **Feature Requests**

### **Feature Request Template**

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

---

## 📚 **Documentation**

### **Documentation Changes**

- Update relevant `.md` files
- Add docstrings to new code
- Include examples for new features
- Keep documentation in sync with code

### **Building Documentation**

```bash
# Install documentation dependencies
pip install -r requirements-dev.txt

# Build docs
cd docs/
make html

# View docs
open _build/html/index.html
```

---

## 🎯 **Priority Areas**

Currently looking for contributions in:

1. **Testing** - Increase test coverage
2. **Documentation** - Improve examples and guides
3. **Performance** - Optimize slow operations
4. **Features** - Walk-forward analysis, ML integration
5. **Bug Fixes** - Address open issues

---

## 🤝 **Community**

- **Questions:** Use GitHub Discussions
- **Bugs:** Create GitHub Issues
- **Features:** Propose in Discussions first
- **Chat:** [Discord/Slack link if applicable]

---

## 📜 **License**

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

## 🙏 **Recognition**

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

**Thank you for contributing to JCAMP Python Backtesting Engine!** 🚀

Your contributions help make this project better for everyone.
