# smartBooks
![CI](https://github.com/trevmanthony/smartBooks/actions/workflows/ci.yml/badge.svg)


## Setup
1. Install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   uvicorn app:app --reload
   ```


## Configuration
The application stores uploaded file records in a SQLite database. By default
the file is created at `data/database.db`, but you can override this location
by setting the `DB_PATH` environment variable:

```bash
DB_PATH=/tmp/custom.db uvicorn app:app --reload
```

See the [FastAPI settings guide](https://fastapi.tiangolo.com/advanced/settings/#environment-variables)
for more on environment-based configuration. For SQLite file management tips,
refer to the [SQLite documentation](https://sqlite.org/whentouse.html).

Uploaded files are stored directly in the local SQLite database as BLOBs.
Each individual upload is limited to 16&nbsp;MB and must use the correct PDF or
CSV MIME type.


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
