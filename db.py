import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "codeeditor")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is not set")

client = MongoClient(MONGODB_URI)
db = client[MONGO_DB_NAME]

snippets = db["code_snippets"]
exec_logs = db["execution_logs"]

def save_code(language: str, code: str) -> str:
    code_id = str(uuid.uuid4())[:8]
    doc = {
        "_id": code_id,
        "language": language,
        "code": code,
        "createdAt": datetime.utcnow(),
        "updatedAt": datetime.utcnow(),
    }
    snippets.insert_one(doc)
    return code_id

def load_code(code_id: str):
    doc = snippets.find_one({"_id": code_id})
    if not doc:
        return None
    return {"language": doc.get("language"), "code": doc.get("code")}

def log_execution(code_id: str, metadata: dict):
    log = {
        "_id": str(uuid.uuid4()),
        "code_id": code_id,
        "language": metadata.get("language"),
        "output": metadata.get("output"),
        "output_type": metadata.get("output_type"),
        "image_path": metadata.get("image_path"),
        "exit_code": metadata.get("exit_code"),
        "error_type": metadata.get("error_type"),
        "execution_time": metadata.get("execution_time"),
        "timestamp": datetime.utcnow(),
    }
    exec_logs.insert_one(log)
