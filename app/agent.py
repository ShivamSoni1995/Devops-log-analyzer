import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from app.prompt import SYSTEM_PROMPT
from app.tools import detect_error_type

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def analyze_log_agent(log: str):
    error_type = detect_error_type(log)

    prompt = f"""{SYSTEM_PROMPT}

Log: {log}
Detected Error Type: {error_type}
"""

    response = model.generate_content(prompt)

    try:
        return json.loads(response.text)
    except:
        return {
            "issue": "Parsing error",
            "cause": response.text,
            "fix": "Check prompt formatting",
            "severity": "Low"
        }
