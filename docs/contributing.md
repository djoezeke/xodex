# Contributing to xodex

Thank you for considering contributing to xodex. This page gives a short
on-ramp to help you get started. See the repository README for full project
policies and the code of conduct.

How to contribute

1. Fork the repository and create a feature branch.
2. Run the test suite (if available) and keep changes small and focused.
3. Open a pull request with a clear description and motivation.

Local development

Install development requirements and run tests locally. Example:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# run the tests
pytest -q
```

Coding guidelines

- Keep public APIs stable and documented in the `docs/` folder.
- Add tests for new features and bug fixes where practical.
- Follow repository style (flake8/black where configured).

Reporting issues

Open an issue on GitHub with a minimal reproduction and the environment you
used (OS, Python version, Pygame version).

Thank you!
