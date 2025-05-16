from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import CodeRequest, CodeResponse
from executor import execute_code
from db import save_code, load_code
from fastapi.responses import JSONResponse
from schemas import HintRequest
from ai_helper import generate_hint
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import PlainTextResponse


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/run", response_model=CodeResponse)
def run_code(code_req: CodeRequest):
    try:
        output = execute_code(code_req.language, code_req.code, code_req.stdin)
        return CodeResponse(output=output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/save")
def save_code_api(code_req: CodeRequest):
    code_id = save_code(code_req.language, code_req.code)
    return {"code_id": code_id}

@app.get("/code/{code_id}")
def load_code_api(code_id: str):
    data = load_code(code_id)
    if not data:
        raise HTTPException(status_code=404, detail="Code not found")
    return data    

@app.post("/ai/hint")
def get_hint(req: HintRequest):
    return {"hint": generate_hint(req.language, req.code)}

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return PlainTextResponse("Rate limit exceeded", status_code=429)

