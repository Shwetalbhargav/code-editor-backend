import subprocess
import os
import uuid
import time

TEMP_DIR = "temp"

def execute_code(language: str, code: str, stdin: str = "") -> dict:
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_id = str(uuid.uuid4())
    ext = "py" if language == "python" else "js"
    filename = os.path.join(TEMP_DIR, f"{temp_id}.{ext}")
    image_path = os.path.join(TEMP_DIR, f"{temp_id}.png")

    # Inject logic to save images for graphical Python code
    if language == "python" and ("matplotlib" in code or "turtle" in code or "tkinter" in code):
        code += f"\nimport matplotlib.pyplot as plt\nplt.savefig('{image_path}')"

    with open(filename, "w") as f:
        f.write(code)

    # Validate language
    if language not in ["python", "javascript"]:
        return {
            "output": "Unsupported language.",
            "output_type": "text",
            "exit_code": -3,
            "error_type": "Unsupported",
            "execution_time": 0.0
        }

    # Direct command (no Docker)
    command = ["python3", filename] if language == "python" else ["node", filename]

    start = time.time()
    try:
        result = subprocess.run(
            command,
            input=stdin.encode(),
            capture_output=True,
            timeout=10
        )
        duration = time.time() - start

        stdout = result.stdout.decode()
        stderr = result.stderr.decode()
        exit_code = result.returncode
        error_type = "RuntimeError" if exit_code != 0 else None

        return {
            "output": stdout + stderr,
            "output_type": "image" if os.path.exists(image_path) else "text",
            "image_path": image_path if os.path.exists(image_path) else None,
            "exit_code": exit_code,
            "error_type": error_type,
            "execution_time": round(duration, 4)
        }

    except subprocess.TimeoutExpired:
        return {
            "output": "Execution timed out.",
            "output_type": "text",
            "exit_code": -1,
            "error_type": "Timeout",
            "execution_time": round(time.time() - start, 4)
        }

    except Exception as e:
        return {
            "output": f"Execution error: {str(e)}",
            "output_type": "text",
            "exit_code": -2,
            "error_type": "Exception",
            "execution_time": round(time.time() - start, 4)
        }
