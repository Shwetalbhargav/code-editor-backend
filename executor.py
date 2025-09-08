import subprocess
import os
import uuid
import time

TEMP_DIR = "temp"

def execute_code(language: str, code: str, stdin: str = "") -> dict:
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_id = str(uuid.uuid4())
    image_path = os.path.join(TEMP_DIR, f"{temp_id}.png")

    # HTML support: just write the file and return its URL path
    if language == "html":
        html_file = os.path.join(TEMP_DIR, f"{temp_id}.html")
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(code)
        return {
            "output": f"/static/{os.path.basename(html_file)}",
            "output_type": "html_url",
            "image_path": None,
            "exit_code": 0,
            "error_type": None,
            "execution_time": 0.0
        }

    ext = "py" if language == "python" else "js"
    filename = os.path.join(TEMP_DIR, f"{temp_id}.{ext}")

    # Inject logic to save images for graphical Python code
    if language == "python" and ("matplotlib" in code or "turtle" in code or "tkinter" in code):
        inject = (
            "\\nimport matplotlib; matplotlib.use('Agg')\\n"
            "import os\\n"
            f"import matplotlib.pyplot as plt\\n"
        )
        code = inject + code + (
            "\\n"
            f"plt.savefig(r'{image_path}') if 'plt' in globals() else None\\n"
            "print('[ImageSaved]')\\n"
        )

    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

    # Direct command (no Docker)
    if language == "python":
        command = ["python3", filename]
    elif language in ("javascript", "js"):
        command = ["node", filename]
    else:
        return {
            "output": "Unsupported language.",
            "output_type": "text",
            "exit_code": -3,
            "error_type": "Unsupported",
            "execution_time": 0.0
        }

    start = time.time()
    try:
        result = subprocess.run(
            command,
            input=stdin.encode("utf-8") if stdin else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=10
        )
        out_text = result.stdout.decode("utf-8", errors="replace")
        output_type = "image" if os.path.exists(image_path) else "text"
        return {
            "output": out_text if output_type == "text" else f"/static/{os.path.basename(image_path)}",
            "output_type": output_type,
            "image_path": f"/static/{os.path.basename(image_path)}" if output_type == "image" else None,
            "exit_code": result.returncode,
            "error_type": None if result.returncode == 0 else "Runtime",
            "execution_time": round(time.time() - start, 4)
        }
    except subprocess.TimeoutExpired:
        return {
            "output": "Execution timed out after 10 seconds.",
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
