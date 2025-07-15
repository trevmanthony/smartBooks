# ADR: Pin httpx below 0.27

## Context
`httpx` 0.27 introduced changes around ASGI/WSGI transports which may break compatibility with some projects relying on FastAPI's `TestClient`. Recent discussions show libraries pinning `httpx==0.27.*` while others require versions >=0.28.

## Decision
For stability we will restrict `httpx` to `<0.27`. This mirrors other projects that locked 0.27 to avoid breaking changes until the ecosystem updates.

## Links
- <https://github.com/encode/httpx/blob/master/CHANGELOG.md#0270-21st-february-2024>
- <https://github.com/huggingface/lighteval/issues/747>
