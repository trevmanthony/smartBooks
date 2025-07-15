# ADR: Provide Default Context for Templates

## Context
The index template expects values like `view_type`, `transaction_type`, and totals.
Providing these defaults in one place avoids repetitive code in route handlers.

## Decision
Create a `render` helper in `app.py` that merges required defaults with per-call
data before calling `TemplateResponse`. This keeps route logic minimal while
guaranteeing the template variables exist.

## Links
- https://fastapi.tiangolo.com/advanced/templates/
- https://www.starlette.io/responses/#templateresponse
- https://testdriven.io/blog/fastapi-jinja2/
