# ADR: Require module docstrings for pylint compliance

## Context
Pylint complains when modules lack docstrings, emitting the `missing-module-docstring` error. Following Python's documentation and linting best practices helps maintain readability and consistency across the codebase.

## Decision
Add short module-level docstrings to test files and other modules as needed so `pylint` passes without `missing-module-docstring` errors. This will be enforced during development and CI runs.

## Links
- <https://peps.python.org/pep-0257/>
- <https://pylint.pycqa.org/en/latest/faq.html>
