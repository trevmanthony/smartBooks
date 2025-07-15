# ADR: Store Uploaded Files as BLOB in SQLite

## Context
Originally the `/upload` endpoint only saved filenames to the database which meant
file contents were lost. We need to keep the actual bytes for later processing
without introducing a new storage service.

## Decision
Extend the `files` table with a `content` BLOB column. When handling an
`UploadFile`, read its contents with `await file.read()` and insert the bytes
using `sqlite3.Binary`. Tests verify that uploaded bytes are persisted and the
`/purge` endpoint removes all records.

## Links
- <https://fastapi.tiangolo.com/tutorial/request-files/>
- <https://docs.python.org/3/library/sqlite3.html#sqlite3.Binary>
- <https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/File_Upload_Cheat_Sheet.md>
