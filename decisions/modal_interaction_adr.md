# ADR: Wait for modal before interacting in tests

## Context
Recent Selenium-based browser tests tried to click the upload button while its Bootstrap modal was still hidden, causing `ElementNotInteractableException` failures.

## Decision
Update the tests to first click the button that triggers the modal and wait until the modal is displayed using Selenium's explicit wait API. Once visible, the test interacts with the file input and upload button.

## Links
- <https://getbootstrap.com/docs/5.3/components/modal/#via-data-attributes>
- <https://www.selenium.dev/documentation/webdriver/waits/#explicit-waits>
