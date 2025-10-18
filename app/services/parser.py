"""Parser module (skeleton) to transform free text to structured filters.

Will rely on LLM to extract candidate filters and then validate via Pydantic
models in app.models.schemas.
"""

from typing import Any


async def parse_filters(text: str) -> dict[str, Any]:
    """Parse text and return candidate filters.

    TODO: call llm_client.extract_filters_from_text and validate with Pydantic.
    """
    return {}
