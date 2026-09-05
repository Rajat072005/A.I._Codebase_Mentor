

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("gemini-3.6-flash")

def generate_answer(prompt):

    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as error:
        print("LLM generation error:", error)
        return None
