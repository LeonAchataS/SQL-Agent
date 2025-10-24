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

    # Enhanced prompt for better conversational extraction
    system_prompt = """Eres un asistente especializado en extraer información de búsqueda de propiedades inmobiliarias.
Tu trabajo es analizar mensajes en lenguaje natural y extraer los filtros de búsqueda en formato JSON.

FILTROS POSIBLES:
- distrito: nombre del distrito (ej: "La Molina", "Palermo", "San Isidro")
- area_min: área mínima en m² (número)
- estado: estado de la propiedad (DISPONIBLE, OCUPADA, MANTENIMIENTO, VENDIDA)
- presupuesto_max: presupuesto máximo (número)
- dormitorios: cantidad de dormitorios (número)
- banios: cantidad de baños (número)
- pet_friendly: acepta mascotas (true/false)
- balcon: tiene balcón (true/false)
- terraza: tiene terraza (true/false)
- amoblado: está amoblado (true/false)

REGLAS:
1. Solo extrae información que esté EXPLÍCITA o IMPLÍCITA en el mensaje
2. Si el usuario menciona "departamento", "depto", "piso" considera que busca propiedades
3. Si menciona un lugar, extrae el distrito
4. Si menciona números de ambientes/habitaciones, extrae dormitorios (ej: "2 ambientes" = 1 dormitorio, "3 ambientes" = 2 dormitorios)
5. Si menciona área (m², metros), extrae area_min
6. Si menciona presupuesto/precio/monto, extrae presupuesto_max
7. NO inventes información que no esté en el mensaje
8. Devuelve SOLO un objeto JSON válido, sin explicaciones adicionales

EJEMPLOS:
Input: "Quiero un departamento en La Molina"
Output: {"distrito": "La Molina"}

Input: "Busco depto de 2 ambientes en Palermo"
Output: {"distrito": "Palermo", "dormitorios": 1}

Input: "Necesito un depto de 80m² con 3 ambientes"
Output: {"area_min": 80, "dormitorios": 2}"""

    user_prompt = f"Mensaje del usuario: {text}\n\nExtrae los filtros en formato JSON:"

    # Use the OpenAI async completion via ChatCompletion.create (requires openai>=1.0)
    try:
        resp = await openai.ChatCompletion.acreate(
            model=settings.llm_model,
            messages=[{"role": "system", "content": system_prompt},
                      {"role": "user", "content": user_prompt}],
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
