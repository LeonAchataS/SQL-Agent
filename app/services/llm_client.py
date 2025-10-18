"""LLM client wrapper using OpenAI async API.

This module performs the minimal task of sending a prompt (extraction) to
OpenAI and returning parsed JSON output. The prompt templates are provided
by the prompts package (when implemented).
"""

from typing import Any
import json
import openai
from app.config import get_settings


settings = get_settings()


async def extract_filters_from_text(text: str) -> dict[str, Any]:
    """Call OpenAI to extract filters from a user message and parse JSON output.

    Expects the model to return a JSON object (as text). This function will try
    to parse the text as JSON and return a dict.
    """
    api_key = settings.openai_api_key
    if not api_key:
        raise RuntimeError("OPENAI API key not configured in settings")

    openai.api_key = api_key

    # Compose a minimal prompt — in production use the full EXTRACT_FILTERS_PROMPT
    prompt = f"Extrae los filtros del mensaje y devuelve solo JSON:\nMensaje: {text}\n"

    # Use the OpenAI async completion via ChatCompletion.create (requires openai>=1.0)
    try:
        resp = await openai.ChatCompletion.acreate(
            model=settings.llm_model,
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
            temperature=settings.llm_temperature,
            max_tokens=500,
        )

        content = resp.choices[0].message.content.strip()

        # Attempt to extract JSON substring (in case the model includes backticks)
        json_start = content.find("{")
        json_end = content.rfind("}")
        if json_start != -1 and json_end != -1 and json_end >= json_start:
            json_text = content[json_start:json_end + 1]
        else:
            json_text = content

        parsed = json.loads(json_text)
        if isinstance(parsed, dict):
            return parsed
        return {}

    except Exception as e:
        # Bubble up exceptions for the caller to handle (agent_service will decide)
        raise
