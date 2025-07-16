# ADR: Add Selenium-based browser tests

## Context
Client-side JavaScript in `index.html` handles file uploads and database purge via fetch requests. We lacked end-to-end tests exercising this logic in a real browser.

## Decision
Introduce Selenium WebDriver running Chrome in headless mode to drive the UI and verify that clicking the upload and purge buttons triggers the corresponding HTTP requests. We use `webdriver-manager` to obtain the appropriate ChromeDriver and rely on Selenium's headless Chrome support. The Docker image installs the libraries required by Chrome.

## Links
- <https://www.selenium.dev/documentation/webdriver/getting_started/>
- <https://github.com/SergeyPirogov/webdriver_manager>
