# ADR: Use Docker container for GitHub Actions CI

## Context
We need a deterministic environment for running linting and tests in CI. Docker images provide reproducible builds. GitHub Actions documentation recommends using Docker for consistent environments, and Docker's documentation describes how to integrate Docker build steps into GitHub Actions.

## Decision
Build a Docker image in the CI workflow and run `black`, `pylint`, and `pytest` inside the container. This ensures the same dependencies and OS are used on every run.

## Links
- https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action
- https://docs.docker.com/build/ci/github-actions/
- https://docs.github.com/en/actions/using-jobs/running-jobs-in-a-container
