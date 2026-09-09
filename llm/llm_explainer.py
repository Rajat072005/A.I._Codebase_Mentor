

import google.generativeai as genai
from dotenv import load_dotenv
import os
from core.api_key_manager import configure_gemini

load_dotenv()
# LOCAL DEVELOPMENT OVERRIDE is now handled inside configure_gemini()
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
_model_name = "gemini-3.6-flash"

_model = genai.GenerativeModel("gemini-3.6-flash")

def generate_answer(prompt):
    configure_gemini()
    _model = genai.GenerativeModel(_model_name)


    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as error:
        print("LLM generation error:", error)
        return None
