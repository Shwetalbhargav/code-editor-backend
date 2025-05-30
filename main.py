from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from schemas import CodeRequest, CodeResponse, HintRequest
from executor import execute_code
from db import save_code, load_code, log_execution
from ai_helper import generate_hint

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return PlainTextResponse("Rate limit exceeded", status_code=429)

@app.post("/run", response_model=CodeResponse)
def run_code(code_req: CodeRequest):
    try:
        result = execute_code(code_req.language, code_req.code, code_req.stdin)
        code_id = save_code(code_req.language, code_req.code)

        # Log execution metadata
        result_with_lang = dict(result)
        result_with_lang["language"] = code_req.language
        result_with_lang["code_id"] = code_id
        log_execution(code_id, result_with_lang)

        return CodeResponse(**result)
    except Exception as e:
        return CodeResponse(
            output=f"Internal server error: {str(e)}",
            output_type="text",
            exit_code=-500,
            error_type="InternalServerError",
            execution_time=0.0
        )

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
    try:
        hint = generate_hint(req.language, req.code)
        return {"hint": hint}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "hint": None,
                "error": "Failed to generate hint",
                "details": str(e)
            }
        )
