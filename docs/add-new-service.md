# Add New Service

## Project Structure

```
expense-rag/
│
├── pyproject.toml          # Main Poetry configuration
├── poetry.lock             # Locked dependencies
├── CHANGELOG.md
│
├── common-lib/             # Shared Python library
│   └── src/common_lib/
│
└── services/               # Microservices
    ├── parser_service/
    ├── rag_service/
    └── auth_service/
```

---

# Development Setup

## Requirements

* Python >= 3.10
* Poetry

Check:

```bash
python --version
poetry --version
```

---

## Install Project

Clone repository:

```bash
git clone <repository-url>
cd expense-rag
```

Install dependencies:

```bash
poetry install
```

Poetry creates the virtual environment and installs:

* FastAPI
* Service dependencies
* common-lib
* Development tools

---

# Running Services

Each service is started from the root folder.

Example:

```bash
poetry run uvicorn services.parser_service.main:app --reload --port 8001
```

Example services:

```bash
# Parser service
poetry run uvicorn services.parser_service.main:app --reload --port 8001

# RAG service
poetry run uvicorn services.rag_service.main:app --reload --port 8002
```

---

# Adding a New Service

## 1. Create service folder

Inside `services`:

```bash
mkdir services/new_service
```

Structure:

```
services/
└── new_service/
    ├── __init__.py
    ├── main.py
    ├── api/
    ├── services/
    ├── models/
    └── repositories/
```

---

## 2. Add FastAPI application

`services/new_service/main.py`

Example:

```python
from fastapi import FastAPI


app = FastAPI()


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
```

---

## 3. Run new service

```bash
poetry run uvicorn services.new_service.main:app --reload --port 8003
```

---

# Adding Dependencies

Do not edit `pyproject.toml` manually.

Use:

```bash
poetry add package-name
```

Example:

```bash
poetry add sqlalchemy
```

For development dependencies:

```bash
poetry add --group dev package-name
```

Example:

```bash
poetry add --group dev pytest
```

Commit:

```
pyproject.toml
poetry.lock
```

---

# Updating common-lib

`common-lib` is shared by all services.

Example:

```
common-lib/
└── src/common_lib/
    ├── logging.py
    ├── middleware.py
    └── config.py
```

After changing common-lib:

Run:

```bash
poetry install
```

Restart FastAPI services.

Test:

```bash
poetry run python -c "import common_lib"
```

---

# Service Communication

Services should not call each other directly from API routes.

Recommended flow:

```
API
 |
 v
Service Layer
 |
 v
Client
 |
 v
Other Service
```

Example:

```
parser_service
        |
        v
rag_service
```

Keep service clients inside:

```
services/<service>/clients/
```

---

# Logging

Use shared logger:

```python
from common_lib.logging import setup_logger

logger = setup_logger("parser-service")

logger.info("Processing started")
logger.debug("Debug information")
logger.exception("Error happened")
```

Configure using:

```
LOG_LEVEL=DEBUG
```

---

# Database Changes

Database code belongs inside the service:

```
service/
├── repositories/
└── models/
```

Do not put database logic in common-lib.

---

# Versioning

Root application version:

`pyproject.toml`

```toml
version = "1.0.0"
```

Service versions are maintained separately if required.

Example:

```
services/parser_service/VERSION
```

```
0.4.0
```

---

# When Code Changes Happen

## Dependency change

Example:

```bash
poetry add new-package
```

Commit:

```
pyproject.toml
poetry.lock
```

---

## common-lib change

Steps:

```bash
poetry install
```

Restart services.

---

## Service code change

No Poetry action needed.

Just restart:

```bash
poetry run uvicorn services.service_name.main:app --reload
```

---

# Before Commit

Run:

```bash
poetry run pytest
```

Format:

```bash
poetry run black .
```

Check types:

```bash
poetry run mypy .
```

---

# Deployment

All services use the same:

```
pyproject.toml
poetry.lock
```

Deployment process:

1. Install dependencies

```bash
poetry install --only main
```

2. Start required services

Example:

```bash
uvicorn services.parser_service.main:app
```

---

# Rules

* Keep business logic inside service
* Keep shared utilities inside common-lib
* Do not duplicate logging/config code
* Do not import code from another service
* Communicate between services using APIs
* Commit `poetry.lock` always
