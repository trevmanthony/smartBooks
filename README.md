# smartBooks

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

## Tests
Run the test suite with:
```bash
pytest
```

## Notes
This project pins `httpx` below version 0.27 due to known compatibility issues.
