# ADR: Attach purgeDatabase to window to replace inline handler

## Context
The Purge DB button used an inline `onclick="purgeDatabase()"` attribute. The JavaScript function was scoped inside `DOMContentLoaded` so it was not accessible globally. MDN notes that [event handler attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes#event_handler_attributes) are a legacy pattern and JavaScript.info [introduction to browser events](https://javascript.info/introduction-browser-events) recommends using methods like `addEventListener` or attaching functions on `window` instead.

## Decision
Expose the `purgeDatabase` function on `window` so the inline attribute resolves correctly. This keeps existing markup but avoids issues with inaccessible handlers. Regression tests verify the HTML button calls the function which performs a `fetch('/purge')` request.

## Links
- https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes#event_handler_attributes
- https://javascript.info/introduction-browser-events
