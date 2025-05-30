from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.staticfiles import StaticFiles
from schemas import CodeRequest, CodeResponse, HintRequest
from executor import execute_code
from db import save_code, load_code, log_execution
from ai_helper import generate_hint
import os


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
app.mount("/static", StaticFiles(directory="temp"), name="static")
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return PlainTextResponse("Rate limit exceeded", status_code=429)

@app.post("/run")
def run_code(code_req: CodeRequest):
    try:
        result = execute_code(code_req.language, code_req.code, code_req.stdin)

        # Extract values
        output = result.get("output", "")
        output_type = result.get("output_type", "text")
        image_url = None

        if output_type == "image" and result.get("image_path"):
            image_filename = os.path.basename(result["image_path"])
            image_url = f"https://code-editor-backend-pync.onrender.com/static/{image_filename}"

        return {
            "output": output,
            "outputType": output_type,
            "imageUrl": image_url,
            "metadata": {
                "executionTime": result.get("execution_time"),
                "exitCode": result.get("exit_code"),
                "errorType": result.get("error_type")
            }
        }

    except Exception as e:
        return {
            "output": f"Server error: {str(e)}",
            "outputType": "text",
            "imageUrl": None,
            "metadata": {
                "executionTime": 0.0,
                "exitCode": -1,
                "errorType": "Exception"
            }
        }

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
