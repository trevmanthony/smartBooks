# ADR: Add regression test for index.html integrity

## Context
`index.html` was truncated, missing closing tags and complete JavaScript logic. We need a regression test to prevent this issue from recurring.

## Decision
Use `BeautifulSoup` to parse the template in tests and verify it ends with `</html>` and contains the success message "Files uploaded successfully!". This approach is lightweight and avoids manual string parsing.

## Links
- <https://html.spec.whatwg.org/multipage/syntax.html#syntax-end-tags>
- <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
- <https://developer.mozilla.org/en-US/docs/Web/API/fetch>

