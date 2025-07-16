# ADR: Docker build excludes tests causing Pylint failure

## Context
The CI workflow builds a Docker image and runs `pylint app.py tests` inside the container. The `.dockerignore` file excludes the `tests/` directory, so Pylint cannot import the `tests` package and exits with `No module named tests`.

## Decision
Excluding `tests/` from the Docker build context leads to this failure. To keep the container consistent with local development, we removed the `tests/` entry from `.dockerignore` so Pylint and pytest run correctly inside Docker.

## Links
- https://docs.docker.com/reference/dockerfile/#dockerignore-file
- https://pylint.pycqa.org/en/latest/user_guide/run.html
- https://docs.docker.com/engine/reference/builder/#dockerignore-file
- https://github.com/pylint-dev/pylint/blob/main/pylint/lint/pylinter.py#L96-L108
