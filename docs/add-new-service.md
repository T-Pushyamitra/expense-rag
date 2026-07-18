# Add New Service

## Current Project Structure

```text
expense-rag/
├── pyproject.toml
├── ruff.toml
├── docker-compose.yml
├── CHANGELOG.MD
├── common-lib/
│   └── src/common_lib/
├── docs/
├── infrastructure/
├── services/
│   ├── embedding_service/
│   │   ├── main.py
│   │   ├── VERSION
│   │   ├── database/
│   │   ├── ollama/
│   │   ├── service/
│   │   └── settings/
│   ├── rag_service/
│   │   └── main.py
│   └── statement_parser_service/
│       ├── main.py
│       ├── VERSION
│       ├── clients/
│       ├── dependency/
│       ├── resources/
│       ├── settings/
│       └── statement_reader/
```

---

# Development Setup

## Requirements

- Python >= 3.10
- Poetry

Check:

```bash
python --version
poetry --version
```

Install dependencies:

```bash
poetry install
```

The workspace uses:

- FastAPI and Uvicorn
- shared package support from common-lib
- Ruff for formatting and linting
- pytest for tests

---

# Running Services

Run services from the repository root.

## Parser service

```bash
poetry run python -m uvicorn services.statement_parser_service.main:app --reload --port 8001
```

## Embedding service

```bash
poetry run python -m uvicorn services.embedding_service.main:app --reload --port 8002
```

## RAG service

```bash
poetry run python -m uvicorn services.rag_service.main:app --reload --port 8003
```

You can also use the Poetry entry points defined in pyproject.toml:

```bash
poetry run statement-parser
poetry run embedding-service
```

---

# Adding a New Service

## 1. Create the service folder

Inside services:

```bash
mkdir services/new_service
```

Recommended layout:

```text
services/
└── new_service/
    ├── __init__.py
    ├── main.py
    ├── clients/
    ├── dependency/
    ├── service/
    ├── settings/
    └── tests/
```

## 2. Add a FastAPI app

Example in services/new_service/main.py:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

## 3. Run the new service

```bash
poetry run python -m uvicorn services.new_service.main:app --reload --port 8004
```

---

# Adding Dependencies

Do not edit pyproject.toml manually.

Use Poetry:

```bash
poetry add package-name
```

For development-only dependencies:

```bash
poetry add --group dev package-name
```

When dependency changes are made, commit both files:

```text
pyproject.toml
poetry.lock
```

---

# Updating common-lib

common-lib is shared by all services.

After changing shared code:

```bash
poetry install
```

Then restart the affected services.

You can verify the shared package import works with:

```bash
poetry run python -c "import common_lib"
```

---

# Service Communication

Keep service-to-service calls behind a client or service layer, not directly inside route handlers.

Recommended flow:

```text
API route
  -> service layer
  -> client/dependency
  -> other service
```

Keep client implementations inside:

```text
services/<service>/clients/
```

---

# Logging

Use the shared logger where possible:

```python
from common_lib.logging import setup_logger

logger = setup_logger("statement-parser")
logger.info("Processing started")
logger.debug("Debug information")
logger.exception("Error happened")
```

Set the log level with:

```bash
LOG_LEVEL=DEBUG
```

---

# Database Changes

Database code should stay inside the service that owns it:

```text
service/
├── database/
├── models/
└── sessions/
```

Do not place database logic in common-lib.

---

# Versioning

The root package version is managed in pyproject.toml:

```toml
version = "1.3.0"
```

Service-specific version files are maintained separately if needed, for example:

```text
services/statement_parser_service/VERSION
```

---

# Before You Commit

Run the checks below before creating a commit:

```bash
poetry run ruff check .
poetry run ruff format .
poetry run pytest
```

If you changed typing-related code, you can also run:

```bash
poetry run mypy .
```

## Recommended commit flow

```bash
git add <files>
git commit -m "<clear commit message>"
```

If you changed formatting or linting config, include the relevant files in the commit:

```text
pyproject.toml
poetry.lock
ruff.toml
```

---

# Deployment

The project uses the same Poetry environment across services.

Install production dependencies with:

```bash
poetry install --only main
```

Then start the required services from the repository root.

---

# Rules

- Keep business logic inside the service.
- Keep shared utilities inside common-lib.
- Do not duplicate logging or configuration code.
- Do not import code from another service directly.
- Prefer API-based communication between services.
- Commit poetry.lock whenever dependencies change.
