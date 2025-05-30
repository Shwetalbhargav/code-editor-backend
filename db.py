from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CodeSnippet, ExecutionLog
from dotenv import load_dotenv
import uuid
import os

# Load from .env
load_dotenv()

USE_DB = True

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def save_code(language: str, code: str) -> str:
    code_id = str(uuid.uuid4())[:8]
    session = SessionLocal()
    snippet = CodeSnippet(id=code_id, language=language, code=code)
    session.add(snippet)
    session.commit()
    session.close()
    return code_id

def load_code(code_id: str):
    session = SessionLocal()
    snippet = session.query(CodeSnippet).filter_by(id=code_id).first()
    session.close()
    if snippet:
        return {"language": snippet.language, "code": snippet.code}
    return None

def log_execution(code_id: str, metadata: dict):
    session = SessionLocal()
    log = ExecutionLog(
        id=str(uuid.uuid4()),
        code_id=code_id,
        language=metadata.get("language"),
        output=metadata.get("output"),
        output_type=metadata.get("output_type"),
        image_path=metadata.get("image_path"),
        exit_code=metadata.get("exit_code"),
        error_type=metadata.get("error_type"),
        execution_time=metadata.get("execution_time"),
    )
    session.add(log)
    session.commit()
    session.close()
