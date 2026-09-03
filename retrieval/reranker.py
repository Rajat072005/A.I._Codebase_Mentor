"""
Gemini Reranker
----------------
Uses Gemini LLM to score each retrieved result (1-10) for relevance
to the user's question. This goes beyond cosine similarity — Gemini
understands context and intent, not just text overlap.
"""

import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_model = genai.GenerativeModel("gemini-2.5-flash")


def rerank_results(question, results):
    """
    Rerank a list of retrieved results using Gemini as a relevance judge.

    Args:
        question : user's question string
        results  : list of result dicts with 'path' and 'content'

    Returns:
        (reranked_results, top_score)
        where top_score is the highest Gemini relevance score (1-10).
    """
    if not results:
        return [], 0

    # Build a readable summary of each result for Gemini to evaluate
    result_text = ""
    for index, result in enumerate(results, start=1):
        result_text += f"""
Result {index}:
Path: {result['path']}
Code:
{result['content']}
"""

    prompt = f"""
Question: {question}

Below are retrieved results from a software repository.

{result_text}

Rate each Result from 1 to 10 based on how relevant it is to answering the question.
10 = highly relevant, 1 = not relevant at all.

Return ONLY valid JSON (no markdown, no explanation):

[
  {{"result": 1, "score": 9}},
  {{"result": 2, "score": 4}}
]
"""

    response = _model.generate_content(prompt)
    cleaned = response.text.strip().replace("```json", "").replace("```", "").strip()

    scores = json.loads(cleaned)
    scores.sort(key=lambda x: x["score"], reverse=True)

    top_score = scores[0]["score"]
    reranked_results = [results[item["result"] - 1] for item in scores]

    return reranked_results, top_score
