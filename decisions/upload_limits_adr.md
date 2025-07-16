# ADR: Enforce File Size and MIME Type Validation

## Context
Previously the `/upload` endpoint only checked the filename extension when accepting files. Without limiting the file size or verifying the MIME type, malicious uploads could exhaust server resources or smuggle unexpected content.

## Decision
Validate each `UploadFile` to ensure the `content_type` is either `application/pdf` or `text/csv`. After reading the file, reject uploads larger than 16 MB. These checks are implemented in `upload_files` and covered by new unit tests.

## Links
- <https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html>
- <https://fastapi.tiangolo.com/tutorial/request-files/>
