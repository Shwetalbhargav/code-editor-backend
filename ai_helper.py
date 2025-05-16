import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_hint(language: str, code: str) -> str:
    prompt = f"Explain this {language} code to a 10-year-old beginner:\n\n{code}\n\nUse a fun and simple tone."
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating hint: {str(e)}"
