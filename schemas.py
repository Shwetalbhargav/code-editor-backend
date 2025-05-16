from pydantic import BaseModel

class CodeRequest(BaseModel):
    language: str  # e.g., "python", "javascript", "html"
    code: str
    stdin: str = ""

class CodeResponse(BaseModel):
    output: str

class HintRequest(BaseModel):
    language: str
    code: str