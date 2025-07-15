# ADR: Add Python .gitignore

## Context
To prevent cached Python files and virtual environments from being committed,
we need a project-level `.gitignore`.

## Decision
Create a `.gitignore` including common patterns such as `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, and `venv/`.

## Links
- <https://github.com/github/gitignore/blob/main/Python.gitignore>
- <https://www.toptal.com/python/beginners-guide-to-python-gitignore>
- <https://docs.github.com/en/get-started/using-git/ignoring-files>
