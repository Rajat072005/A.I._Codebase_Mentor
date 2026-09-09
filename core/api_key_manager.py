import os

import google.generativeai as genai
from dotenv import load_dotenv
from flask import has_request_context, request

load_dotenv()

def configure_gemini():
    """
    Configures the Gemini API client dynamically using the X-Gemini-Key header
    if available. Falls back to the local .env key.
    """
    api_key = None
    
    if has_request_context():
        # Bring Your Own Key (BYOK) mode
        api_key = request.headers.get("X-Gemini-Key")
        
    if not api_key:
        # LOCAL DEVELOPMENT OVERRIDE fallback
        api_key = os.getenv("GEMINI_API_KEY")
        
    if api_key:
        genai.configure(api_key=api_key)
        return True
    
    print("WARNING: No Gemini API key found in headers or .env!")
    return False

