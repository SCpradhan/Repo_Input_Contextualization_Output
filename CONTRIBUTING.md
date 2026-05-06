# Contributing to AAVA AI

Thank you for your interest in contributing to AAVA AI!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Run tests: `pytest tests/`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature`
8. Create a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio black flake8 mypy

# Run tests
pytest tests/

# Format code
black .

# Lint
flake8 .
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions focused and small
- Add tests for new features

## Adding New Agents

1. Create agent file in `agents/`
2. Inherit from `BaseAgent`
3. Implement `analyze()` method
4. Add tests in `tests/`
5. Update configuration
6. Document in README

## Testing

- Write unit tests for all new code
- Use pytest fixtures for common setup
- Test edge cases and error handling
- Aim for >80% code coverage

## Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for design changes
- Add docstrings to all functions
- Include usage examples

## Pull Request Process

1. Update documentation
2. Add tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Questions?

Open an issue or reach out to the maintainers.
