import subprocess
import os
import uuid

TEMP_DIR = "temp"

def execute_code(language: str, code: str, stdin: str = "") -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)
    temp_id = str(uuid.uuid4())

    if language in ["python", "javascript"]:
        ext = "py" if language == "python" else "js"
        filename = os.path.join(TEMP_DIR, f"{temp_id}.{ext}")
        with open(filename, "w") as f:
            f.write(code)

        try:
            if language == "python":
                result = subprocess.run(
                    ["python", filename],
                    input=stdin.encode(),
                    capture_output=True,
                    timeout=5
                )
            else:  # javascript
                result = subprocess.run(
                    ["node", filename],
                    input=stdin.encode(),
                    capture_output=True,
                    timeout=5
                )
            return result.stdout.decode() + result.stderr.decode()

        except subprocess.TimeoutExpired:
            return "Execution timed out."
        except Exception as e:
            return f"Execution error: {str(e)}"

    elif language == "html":
        return "HTML code received. Render it on the frontend."

    return "Unsupported language."
