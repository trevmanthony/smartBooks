# ADR: Stubbed pipeline without llama-cpp

## Context
The prototype LangChain pipeline included `llama-cpp-python` for running the o4-mini model locally. Building this dependency requires a C/C++ compiler and CMake, which caused Docker builds to fail on minimal environments.

## Decision
Temporarily drop `llama-cpp-python` and keep the `AsyncPipeline` using stubbed OCR and LLM clients that return canned values for tests. The Docker image now installs `cmake` and `g++` to support potential future native builds if needed.

## Links
- https://platform.openai.com/docs/models/o4-mini
- https://raw.githubusercontent.com/abetlen/llama-cpp-python/master/README.md
