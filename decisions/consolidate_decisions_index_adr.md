# ADR: Consolidate decisions folder and add index

## Context
The `decisions` directory contains many ADR files, some of which address the same topic. Over time it became hard to know which ADRs are current.

Industry guidance recommends keeping ADRs organized and clearly marking superseded documents.

## Decision
We will add a `README.md` inside the `decisions` folder listing all ADRs. Conflicting ADRs will be marked as superseded, but the original files remain for history.

References consulted:
- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Architecture Decision Records](https://martinfowler.com/articles/architecture-decision-records.html)

We also add a task to `TODO.md` to review outdated Docker ADRs.

## Links
- https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- https://martinfowler.com/articles/architecture-decision-records.html
