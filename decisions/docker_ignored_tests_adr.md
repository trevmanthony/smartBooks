# ADR: Docker build excludes tests causing Pylint failure

## Context
The CI workflow builds a Docker image and runs `pylint app.py tests` inside the container. The `.dockerignore` file excludes the `tests/` directory, so Pylint cannot import the `tests` package and exits with `No module named tests`.

## Decision
Document that excluding `tests/` from the Docker build context leads to this failure. Pylint expects modules to be importable, so either include `tests/` in the image or avoid running Pylint on the tests package in Docker.

## Links
- https://docs.docker.com/reference/dockerfile/#dockerignore-file
- https://pylint.pycqa.org/en/latest/user_guide/run.html
