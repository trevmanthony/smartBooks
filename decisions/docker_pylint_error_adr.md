# ADR: Pylint error when running tests in Docker

## Context
Running the Docker command `pylint app.py tests` failed with `No module named tests` because the container's working directory did not include the Python path for the `tests` package. Pylint expects modules to be importable to analyze them.

## Decision
Document the error and reference official guidance on setting the Python path correctly when running Pylint inside Docker.

## Links
- https://pylint.pycqa.org/en/latest/user_guide/run.html
- https://docs.python.org/3/tutorial/modules.html#packages
