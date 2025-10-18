"""LLM client wrapper (skeleton).

This module will encapsulate calls to the LLM (OpenAI or other). Keep a thin
wrapper that returns structured outputs when possible.
"""

from typing import Any


async def extract_filters_from_text(text: str) -> dict[str, Any]:
    """Call LLM to extract filters from a user message.

    Returns a dictionary shaped like the Filter Pydantic model (to be defined).
    """
    # NOTE: This function is intentionally left as a stub so tests can mock it.
    # Implementations should call the LLM with the EXTRACT_FILTERS_PROMPT and
    # return a JSON-serializable dict with the extracted keys/values.
    raise NotImplementedError("LLM client not implemented; mock this function in tests or implement an OpenAI call")
