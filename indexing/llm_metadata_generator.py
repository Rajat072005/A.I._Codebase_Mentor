"""
LLM Metadata Generator
-----------------------
Uses Gemini to generate rich semantic metadata for a single source code file.

Metadata includes:
  - purpose         : What the file does (1-2 sentences)
  - responsibilities: 3-5 high-level responsibilities
  - concepts        : 3-6 key software engineering concepts
  - keywords        : 5-10 retrieval-friendly keywords

This is the single-file fallback used by llm_metadata_batch_generator.py
when a batch fails at the smallest granularity.
"""

import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("gemini-3.6-flash")

_PROMPT_TEMPLATE = """
You are an expert software architect analyzing a source code file.

Generate structured metadata for the file below.

Return ONLY valid JSON (no markdown, no explanation) with this exact shape:
{{
  "purpose": "one or two sentences describing what this file does",
  "responsibilities": ["responsibility 1", "responsibility 2", "..."],
  "concepts": ["concept 1", "concept 2", "..."],
  "keywords": ["keyword1", "keyword2", "..."]
}}

Rules:
- purpose        : 1-2 sentences, architectural focus
- responsibilities: 3-5 items, high-level only
- concepts       : 3-6 software engineering concepts present in this file
- keywords       : 5-10 retrieval-friendly terms a developer might search for

Source code:

{file_content}
"""


def generate_llm_metadata(file_content):
    """
    Generate semantic metadata for a single source file using Gemini.

    Args:
        file_content : raw text content of the file

    Returns:
        A dict with keys: purpose, responsibilities, concepts, keywords.
    """
    prompt = _PROMPT_TEMPLATE.format(file_content=file_content)
    response = _model.generate_content(prompt)

    cleaned = response.text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    return json.loads(cleaned)

