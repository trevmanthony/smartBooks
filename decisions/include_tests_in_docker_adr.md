# ADR: Include tests in Docker build for Pylint

## Context
Earlier, `.dockerignore` excluded the `tests/` directory. When the CI workflow built the Docker image and ran `pylint app.py tests`, Pylint failed to import the `tests` package, reporting `No module named tests`.

## Decision
We removed the `tests/` entry from `.dockerignore` so tests are copied into the Docker build context. This allows Pylint inside the container to import the modules and run successfully.

## Links
- https://docs.docker.com/engine/reference/builder/#dockerignore-file
- https://pylint.pycqa.org/en/latest/user_guide/run.html
