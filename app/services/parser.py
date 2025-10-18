"""Parser module (skeleton) to transform free text to structured filters.

Will rely on LLM to extract candidate filters and then validate via Pydantic
models in app.models.schemas.
"""

from typing import Any
from app.services import llm_client
from app.models.schemas import FilterEssential, FilterOptional


async def parse_filters(text: str, current_filters: dict | None = None) -> dict[str, Any]:
    """Parse text and return candidate filters.

    - Calls the LLM client (mockable) to extract filters as JSON
    - Validates and returns merged filters (only the keys present)
    """
    current_filters = current_filters or {}

    # Call LLM client to get extraction (tests will mock this function)
    raw = await llm_client.extract_filters_from_text(text)

    if not isinstance(raw, dict):
        # If LLM returned unexpected format, return empty
        return {}

    # Validate essentials and optionals separately, ignoring missing keys
    essentials = {}
    optionals = {}

    # Filter raw keys for essentials
    essential_fields = {f.name for f in FilterEssential.model_fields.values()} if hasattr(FilterEssential, 'model_fields') else {"distrito", "area_min", "estado", "presupuesto_max", "dormitorios"}
    optional_fields = {f.name for f in FilterOptional.model_fields.values()} if hasattr(FilterOptional, 'model_fields') else {"pet_friendly", "balcon", "terraza", "amoblado", "banios"}

    for k, v in raw.items():
        if k in essential_fields:
            essentials[k] = v
        elif k in optional_fields:
            optionals[k] = v

    # Validate using Pydantic by creating models with existing values (this will coerce types)
    validated = {}
    if essentials:
        try:
            fe = FilterEssential(**{**(current_filters or {}), **essentials})
            # Only include keys that were present in the raw extraction
            for key in essentials.keys():
                validated[key] = getattr(fe, key)
        except Exception:
            # If validation fails, ignore essentials
            pass

    if optionals:
        try:
            fo = FilterOptional(**{**(current_filters or {}), **optionals})
            for key in optionals.keys():
                validated[key] = getattr(fo, key)
        except Exception:
            # Ignore optionals if validation fails
            pass

    return validated
