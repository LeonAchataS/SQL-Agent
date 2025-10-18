"""NLP helper functions: normalization, number parsing, currency parsing.

Small utilities used by parser and llm prompts.
"""

def normalize_text(text: str) -> str:
    return text.strip()
