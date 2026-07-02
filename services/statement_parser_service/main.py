from fastapi import FastAPI, File, UploadFile
from dotenv import load_dotenv
import os

from .statement_reader.statement_reader_factory import StatementReaderFactory
from pathlib import Path
import tempfile
import shutil
import uvicorn

from common_lib import setup_logger

load_dotenv()

from pathlib import Path

SERVICE_VERSION = (
    Path(__file__).parent / "VERSION"
).read_text().strip()
    

app = FastAPI(
    title="Statement Parser Service",
    description="A service for parsing financial statements",
    version=SERVICE_VERSION
)


@app.get("/")
def root():
    return {
        "service": "statement-parser-service",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/parse")
async def parse(file: UploadFile | None = File(...), password: str = 201150838):
    try:
        # create temporary directory
        temp_dir = Path(tempfile.mkdtemp())
        
        # create temp file path
        file_path = temp_dir / file.filename

        # save uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )
        statementReader = StatementReaderFactory.get_reader('Hdfc', str(file_path), password)
        metadata = statementReader.reader()

        return {
            "Message": "Success",
            "metadata": metadata
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def run():
    uvicorn.run(
        "services.statement_parser_service.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=True
    )