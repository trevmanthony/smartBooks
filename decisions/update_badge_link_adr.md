# ADR: Use actual GitHub repo path in CI badge

## Context
The README initially included a CI status badge pointing to `https://github.com/OWNER/REPO/...` as a placeholder. This produced a broken link. GitHub documentation shows how to form workflow badges with the repository's `owner/repo` path. Shields.io also documents generating status badges for GitHub workflows.

## Decision
Update the README badge URL to `https://github.com/trevmanthony/smartBooks/actions/workflows/ci.yml/badge.svg` so it reflects the real repository path and displays workflow status correctly.

## Links
- <https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge>
- <https://github.com/badges/shields>
