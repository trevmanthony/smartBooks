# ADR: Clarify Contributor Guidelines

## Context
The existing `AGENTS.md` lacked specifics around task tracking, audit log usage, commit message style, and pull request expectations.

## Decision
- Document adding new tasks to `TODO.md` using unchecked `- [ ]` bullets.
- Reference `decisions/audit_log_adr.md` and show an example JSON log entry.
- Require commit messages to use a short imperative summary referencing one ticket.
- Mention that tests must maintain full coverage as enforced by CI.
- State that each task should be developed on a feature branch and submitted via pull request.

## Links
- <https://chris.beams.io/posts/git-commit/>
- <https://jsonlines.org/>
- <https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests>
