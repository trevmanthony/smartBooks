Rule 0 – Research relentlessly
For every task, gather at least two recent, credible sources and save the links in an ADR under /decisions/.

Rule 1 – One goal per task
Limit each task to a single measurable goal and provide a clear pass/fail check that must succeed.

Rule 2 – No scope creep
If new requirements appear during a task, finish the current goal first, add the new item as an unchecked `- [ ]` entry in the root `TODO.md`, and wait for a separate task before working on it.

Rule 3 – Plan before coding
For every task, first propose 2–3 researched implementation options with brief pros/cons and wait for human approval before making code changes.

Rule 4 – Audit log
For every data mutation or code change, append a JSONL record to `/logs/actions.jsonl` describing the action, timestamp, and task ID. See `decisions/audit_log_adr.md` for details. A typical entry:
`{"timestamp": "2025-07-15T20:22:20Z", "action": "Add feature", "ticket_id": "task-example"}`. Migrate to a database table only if log size or query needs demand it.

Rule 5 – Keep dependencies in sync
Whenever code adds or removes a library, update every relevant manifest file (e.g., requirements.txt, package.json, pyproject.toml, etc.) and verify the project builds cleanly from a fresh workspace.

Rule 6 – Ship stable tests
Every code change must add or update automated tests that cover the new logic; flag flaky tests appropriately for the testing framework (e.g., `xfail(strict=True)` in pytest) and keep coverage at 100% as enforced by `.github/workflows/ci.yml`.

Rule 7 – Protect secrets
Never hard-code credentials. Store all keys/tokens in your environment’s secrets manager (e.g., GitHub Actions Secrets, AWS Parameter Store, HashiCorp Vault) and load them via environment variables; record secret usage in /logs/actions.jsonl without exposing the value.

Rule 8 – Enforce code style
Run an auto-formatter (e.g., Black for Python, Prettier for JS) and a linter (e.g., Pylint or ESLint) appropriate to the language on every change; commit only code that passes formatting and lint checks.

Rule 9 – CI must pass
Each task is complete only when the project’s defined CI pipeline (e.g., GitHub Actions, Azure Pipelines) passes all steps—build, tests, formatter, and linter checks.

Rule 10 – Update documentation
If a change affects external behavior—API endpoints, CLI flags, environment variables, or user-visible workflows—update the relevant README or /docs/*.md files before completing the task.

Rule 11 – Commit and PR conventions
Write commit messages in imperative mood with a short (about 50 characters) summary referencing a single ticket ID. Develop each task on its own branch and open a pull request once CI passes.
