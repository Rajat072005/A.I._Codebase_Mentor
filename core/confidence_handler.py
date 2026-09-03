"""
Confidence Handler
-------------------
Decides whether we have enough evidence to answer a question.
Uses the top Gemini reranker score (1-10) compared against a
per-strategy confidence threshold.
"""


def should_answer(top_score, threshold: int = 7) -> bool:
    """
    Return True if the top retrieved chunk/file score meets the threshold.
    The threshold comes from the strategy config so different intents
    can have different confidence requirements.
    """
    return top_score >= threshold


def build_low_confidence_message(question: str) -> str:
    """
    Return a friendly message when confidence is too low to answer.
    """
    return f"""
I couldn't find enough relevant evidence in this repository to confidently answer:

"{question}"

Possible reasons:
• This feature may not exist in the repository.
• It may be implemented under a different name or file.
• The repository may contain only part of the system (e.g. frontend only).
• Try rephrasing using a file name, component name, or specific keyword.

No answer was generated to avoid making incorrect assumptions.
"""
