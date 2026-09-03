"""
LLM Metadata Generator
------------------------
Calls Gemini to analyze a source file and generate structured metadata:
  - purpose        : one sentence describing what this file does
  - responsibilities : 3-5 high-level responsibilities
  - concepts       : 3-6 software engineering concepts present
  - keywords       : 5-10 retrieval-friendly keywords

This metadata gets stored in the metadata cache and used to build
knowledge documents, which dramatically improve retrieval quality.
"""

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("gemini-2.5-flash")

_PROMPT_TEMPLATE = """
You are an expert software architect analyzing a source code file.

Your task: generate structured metadata that will be used to improve
semantic retrieval in an AI code understanding system.

Rules:
1. Analyze only the provided file.
2. Do not assume functionality that is not visible in the file.
3. Focus on architectural understanding rather than line-by-line implementation.
4. Keep every field concise but meaningful.
5. The purpose must contain exactly one or two sentences.
6. Responsibilities must contain between 3 and 5 high-level responsibilities.
7. Concepts must contain between 3 and 6 important software engineering concepts.
8. Keywords must contain between 5 and 10 retrieval-friendly keywords.
9. Return only valid JSON. No markdown. No explanation outside the JSON.

Output format:
{{
    "purpose": "",
    "responsibilities": [],
    "concepts": [],
    "keywords": []
}}

Source Code:

{file_content}
"""


def generate_llm_metadata(file_content):
    """
    Generate structured metadata for a source file using Gemini.
    Returns a dict or None if parsing fails.
    """
    prompt = _PROMPT_TEMPLATE.format(file_content=file_content)
    raw_response = _model.generate_content(prompt).text

    # Strip markdown code fences if Gemini wraps the JSON
    clean = raw_response.strip()
    if clean.startswith("```json"):
        clean = clean.replace("```json", "").replace("```", "").strip()
    elif clean.startswith("```"):
        clean = clean.replace("```", "").strip()

    try:
        return json.loads(clean)
    except Exception as e:
        print(f"Metadata parsing failed: {e}")
        return None
