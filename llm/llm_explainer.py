"""
LLM Explainer
--------------
Sends the assembled prompt to Gemini and returns the generated answer.
This is the final step in the Q&A pipeline.
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("gemini-2.5-flash")


def generate_answer(prompt):
    """
    Send a prompt to Gemini and return the text response.
    Returns None if the call fails.
    """
    try:
        response = _model.generate_content(prompt)
        return response.text
    except Exception as error:
        print("LLM generation error:", error)
        return None
