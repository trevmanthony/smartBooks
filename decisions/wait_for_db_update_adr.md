# ADR: Wait for DB update in Selenium tests

## Context
During CI the Selenium-based browser test occasionally failed because the database update triggered by the fetch upload request completed slightly after the success message appeared. The test immediately checked the database and saw zero records.

## Decision
Use `WebDriverWait` to poll until the `files` table shows the expected count after the upload and purge actions. This follows Selenium's explicit wait guidance and accounts for asynchronous fetch behavior.

## Links
- https://selenium.dev/documentation/webdriver/waits/#explicit-waits
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch
