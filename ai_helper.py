import re
from textwrap import dedent

def _summarize_python(code: str):
    points = []
    if "def " in code:
        funcs = re.findall(r"def\s+([a-zA-Z_]\w*)\s*\(", code)
        if funcs:
            points.append(f"Defines function(s): {', '.join(funcs)}.")
    if "class " in code:
        classes = re.findall(r"class\s+([a-zA-Z_]\w*)\s*(?:\(|:)", code)
        if classes:
            points.append(f"Creates class(es): {', '.join(classes)}.")
    if "for " in code:
        points.append("Uses a for-loop to repeat steps.")
    if "while " in code:
        points.append("Uses a while-loop which repeats until a condition is false.")
    if "if " in code:
        points.append("Checks conditions with if/elif/else to make decisions.")
    if "print(" in code:
        points.append("Shows messages using print().")
    if "input(" in code:
        points.append("Reads text from the user using input().")
    if "import " in code:
        points.append("Brings in extra tools with import.")
    if "matplotlib" in code or "plt." in code:
        points.append("Draws a picture/graph using matplotlib.")
    if "turtle" in code:
        points.append("Uses turtle to draw shapes on the screen.")
    return points

def _summarize_js(code: str):
    points = []
    if "function " in code or "=>" in code:
        points.append("Defines functions to group steps together.")
    if "console.log" in code:
        points.append("Prints messages using console.log.")
    if "for" in code:
        points.append("Uses a for-loop to do something many times.")
    if "while" in code:
        points.append("Repeats with a while-loop until a rule is met.")
    if ("if(" in code) or (" if " in code):
        points.append("Makes choices with if/else.")
    if "fetch(" in code or "XMLHttpRequest" in code:
        points.append("Gets data from the internet with fetch (an HTTP request).")
    return points

def _summarize_html(code: str):
    points = []
    if "<canvas" in code:
        points.append("Draws on a 2D canvas in the page.")
    if "<script" in code:
        points.append("Runs JavaScript inside the page.")
    if "<style" in code or "style=" in code:
        points.append("Styles the page with CSS.")
    if "<form" in code:
        points.append("Collects user input with a form.")
    if "<img" in code:
        points.append("Shows an image on the page.")
    return points

def generate_hint(language: str, code: str) -> str:
    language = (language or "").strip().lower()
    code = code or ""

    opener = f"Here’s your {language or 'code'} explained like you’re 10:\n\n"
    if language == "python":
        bullets = _summarize_python(code)
    elif language in ("javascript", "js", "node"):
        bullets = _summarize_js(code)
    elif language == "html":
        bullets = _summarize_html(code)
    else:
        bullets = []

    if not bullets:
        bullets = ["It runs step by step from top to bottom.",
                   "It uses variables to remember values.",
                   "It can make choices and repeat actions."]

    result = opener + "\n".join(f"• {b}" for b in bullets)
    result += dedent("""

        \nWhat you can try next:
        • Change a value and see how the result changes.
        • Add a print/log line to watch what happens.
        • If you see an error, read the last line — it often says exactly what went wrong.
    """).rstrip()
    return result
