# ADR: Update Agent Guidelines

## Context
Feedback showed that the assistant needed more explicit direction to record new tasks in `TODO.md`. Additionally, the assistant does not control branching or pull requests, so the previous rule around PR workflow caused confusion.

## Decision
- Encourage creating `TODO.md` entries whenever new requirements emerge.
- Remove the rule requiring branch and PR management because it is outside of the assistant's scope.

## Links
- <https://google.github.io/styleguide/pyguide.html#312-todo-comments>
- <https://chris.beams.io/posts/git-commit/>
