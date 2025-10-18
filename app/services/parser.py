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

    # Normalization mapping: allow Spanish keys commonly found in previous project
    key_map = {
        "monto_maximo": "presupuesto_max",
        "monto": "presupuesto_max",
        "presupuesto": "presupuesto_max",
        "estado_propiedad": "estado",
        "permite_mascotas": "pet_friendly",
        "banios": "banios",
        "baños": "banios",
        "area": "area_min",
        "area_min": "area_min",
        "distrito": "distrito",
        "dormitorios": "dormitorios",
        "balcon": "balcon",
        "terraza": "terraza",
        "amoblado": "amoblado",
    }

    for k, v in raw.items():
        mapped_key = key_map.get(k, k)
        # Decide if mapped_key belongs to essentials or optionals by checking model fields
        if mapped_key in FilterEssential.model_fields:
            essentials[mapped_key] = v
        elif mapped_key in FilterOptional.model_fields:
            optionals[mapped_key] = v
        else:
            # Unknown key - ignore for now
            pass

    # Validate using Pydantic by creating models with existing values (this will coerce types)
    validated = {}
    if essentials:
        try:
            # Coerce types for essentials
            coerced_essentials = {}
            for kk, vv in essentials.items():
                if isinstance(vv, str) and vv.replace('.', '', 1).isdigit():
                    # numeric string
                    coerced_essentials[kk] = float(vv) if '.' in vv else int(vv)
                else:
                    coerced_essentials[kk] = vv

            fe = FilterEssential(**{**(current_filters or {}), **coerced_essentials})
            # Only include keys that were present in the raw extraction
            for key in essentials.keys():
                validated[key] = getattr(fe, key)
        except Exception:
            # If validation fails, ignore essentials
            pass

    if optionals:
        try:
            # Coerce optionals booleans and numbers
            coerced_optionals = {}
            for kk, vv in optionals.items():
                if isinstance(vv, str):
                    lv = vv.strip().lower()
                    if lv in {"true", "yes", "si", "sí", "1", "s"}:
                        coerced_optionals[kk] = True
                        continue
                    if lv in {"false", "no", "0", "n"}:
                        coerced_optionals[kk] = False
                        continue
                    if lv.replace('.', '', 1).isdigit():
                        coerced_optionals[kk] = float(vv) if '.' in vv else int(vv)
                        continue
                    coerced_optionals[kk] = vv
                else:
                    coerced_optionals[kk] = vv

            fo = FilterOptional(**{**(current_filters or {}), **coerced_optionals})
            for key in optionals.keys():
                validated[key] = getattr(fo, key)
        except Exception:
            # Ignore optionals if validation fails
            pass

    return validated
