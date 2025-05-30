import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_hint(language: str, code: str) -> str:
    prompt = f"Explain this {language} code to a 10-year-old beginner:\n\n{code}\n\nUse a fun and simple tone."

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_ENDPOINT, json=payload)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text'].strip()
        else:
            return f"[Gemini API Error {response.status_code}] {response.text}"
    except requests.exceptions.RequestException as e:
        return f"[HintGenerationError] Request failed: {str(e)}"
    except Exception as e:
        return f"[HintGenerationError] Unexpected error: {str(e)}"
