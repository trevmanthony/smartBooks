# smartBooks
![CI](https://github.com/trevmanthony/smartBooks/actions/workflows/ci.yml/badge.svg)


## Setup
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --no-cache-dir -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

### Updating dependencies
Install pip-tools and recompile the lock file when updating packages:
```bash
pip install --no-cache-dir pip-tools
pip-compile requirements.in --output-file requirements.txt
```


## Configuration
The application reads configuration from environment variables using a
Pydantic `Settings` class. Uploaded file records are stored in a SQLite
database. By default the file is created at `data/database.db`, but you can
override this location with the `DB_PATH` variable. The maximum allowed upload
size can also be changed via `MAX_FILE_SIZE`:

```bash
DB_PATH=/tmp/custom.db MAX_FILE_SIZE=$((8*1024*1024)) uvicorn app:app --reload
```

See the [FastAPI settings guide](https://fastapi.tiangolo.com/advanced/settings/#environment-variables)
for more on environment-based configuration. For SQLite file management tips,
refer to the [SQLite documentation](https://sqlite.org/whentouse.html).

Uploaded files are stored directly in the local SQLite database as BLOBs.
Each individual upload is limited to 16&nbsp;MB and must use the correct PDF or
CSV MIME type.

The `/process/{id}` endpoint triggers a background task that runs the uploaded
document through an OCR and LLM pipeline. The prototype uses stub clients to
demonstrate asynchronous processing with FastAPI `BackgroundTasks`.


To run the full pipeline with Document AI and o4-mini, set the following environment variables:

```bash
DOC_AI_PROJECT_ID=<your-project>
DOC_AI_LOCATION=<region>  # optional
DOC_AI_PROCESSOR_ID=<processor-id>
O4MINI_MODEL_PATH=/path/to/o4-mini.gguf
```

Then call `pipeline.create_langchain_pipeline()` in place of the stubs.

## Tests
Run the test suite with:
```bash
pytest
```

## Notes
This project pins `httpx` below version 0.27 due to known compatibility issues.


All pull requests must pass the CI workflow.

## License
This project is licensed under the [MIT License](./LICENSE).
