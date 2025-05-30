from pydantic import BaseModel
from typing import Optional

class CodeRequest(BaseModel):
    language: str  # e.g., "python", "javascript", "html"
    code: str
    stdin: str = ""

class CodeResponse(BaseModel):
    output: str
    output_type: str = "text"
    image_path: Optional[str] = None
    exit_code: Optional[int] = None
    error_type: Optional[str] = None
    execution_time: Optional[float] = None

class HintRequest(BaseModel):
    language: str
    code: str
