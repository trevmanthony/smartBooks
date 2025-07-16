# ADR: Use Celery Eager Mode in Tests

## Context
Running Celery tasks through a broker slowed down and complicated our test suite. Enabling eager mode lets tests execute tasks synchronously without Redis.

## Decision
Set the environment variable `CELERY_TASK_ALWAYS_EAGER` in tests so Celery executes tasks locally. This keeps the test environment self-contained while mimicking production behavior.

## Links
- <https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-always-eager>
- <https://docs.celeryq.dev/en/stable/userguide/tasks.html>
