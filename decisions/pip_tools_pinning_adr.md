# ADR: Pin dependencies with pip-tools

## Context
To ensure stable environments across CI and Docker builds, we need fully pinned versions for all Python libraries. The Python Packaging guide recommends using pinned requirement files for repeatability. We also disable pip caching to avoid stale wheels.

## Decision
Introduce `pip-tools` to compile `requirements.txt` from a new `requirements.in`. CI installs pip-tools with `--no-cache-dir`, compiles the lock file, and installs from it before building the Docker image.

## Links
- https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/
- https://pip.pypa.io/en/stable/topics/caching/#disabling-caching
- https://pip-tools.readthedocs.io/en/latest/
