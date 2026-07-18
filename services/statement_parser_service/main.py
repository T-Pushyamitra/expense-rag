import os
import shutil
import tempfile
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, File, UploadFile, status
from pydantic import BaseModel

from .clients import HttpEmbeddingClient
from .dependency.embedding_client import get_embedding_client
from .settings import SETTINGS
from .statement_reader.common.statement_exceptions import (
    CorruptedPdfException,
    InvalidPasswordException,
    StatementReaderException,
    UnsupportedFileException,
)
from .statement_reader.common.statement_reader_factory import StatementReaderFactory
from .statement_reader.common.transaction_utils import Transaction

SERVICE_VERSION = (Path(__file__).parent / "VERSION").read_text().strip()


app = FastAPI(title=SETTINGS.app_name, description=SETTINGS.app_description, version=SERVICE_VERSION)


#### API RESPONSE
class ErrorModel(BaseModel):
    message: str


class TransactionResponse(BaseModel):
    status: int
    data: list[Transaction] | None = None
    error: ErrorModel | None = None


@app.get("/")
def root():
    return {"service": SETTINGS.app_name, "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/parse")
def parse(
    file: UploadFile | None = File(...),
    bank: str = None,
    password: str = 201150838,
    client: HttpEmbeddingClient = Depends(get_embedding_client),
):
    try:
        # create temporary directory
        temp_dir = Path(tempfile.mkdtemp())

        # create temp file path
        file_path = temp_dir / file.filename

        # save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        statementReader = StatementReaderFactory.get_reader(bank, str(file_path), password)

        transactions = statementReader.reader()

        embedding_response = client.embed_transactions(transactions)

        if embedding_response["status"] != 200:
            raise StatementReaderException("Failed to embedding the pdf file. Try again!")

        return TransactionResponse(
            status=status.HTTP_200_OK,
            data=transactions,
        )

    except UnsupportedFileException as e:
        return TransactionResponse(
            status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message=f"{type(e).__name__} : {e.message}")
        )

    except InvalidPasswordException as e:
        return TransactionResponse(
            status=status.HTTP_401_UNAUTHORIZED, error=ErrorModel(message=f"{type(e).__name__} : {e.message}")
        )

    except CorruptedPdfException as e:
        return TransactionResponse(
            status=status.HTTP_406_NOT_ACCEPTABLE, error=ErrorModel(message=f"{type(e).__name__} : {e.message}")
        )

    except Exception as e:
        return TransactionResponse(
            status=status.HTTP_400_BAD_REQUEST, error=ErrorModel(message=f"{type(e).__name__} : {str(e)}")
        )
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def run():
    uvicorn.run(
        "services.statement_parser_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", SETTINGS.app_port)),
        reload=True,
        reload_dirs=["services/statement_parser_service", "common_lib"],
    )
