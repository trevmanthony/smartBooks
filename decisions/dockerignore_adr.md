# ADR: Add .dockerignore

## Context
Docker builds were including test files and local virtual environments, leading to larger image sizes and potential leakage of development artifacts.

## Decision
Add a `.dockerignore` file excluding `.git`, `__pycache__/`, `.pytest_cache/`, `tests/`, and local virtual environment directories. This follows Docker's best practices for minimizing build context.

## Links
- <https://docs.docker.com/develop/dev-best-practices/#dockerignore>
- <https://docs.docker.com/engine/reference/builder/#dockerignore-file>
- <https://www.docker.com/blog/7-best-practices-for-writing-dockerfiles/>
