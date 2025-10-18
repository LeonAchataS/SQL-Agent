"""Agent orchestrator service (skeleton).

Responsibilities:
- Orchestrate session state and dialog flow
- Use parser to extract filters
- Use query_builder to build parametric SQL
- Use db to execute queries with retries

All functions are placeholders. Implementation will come later.
"""

from typing import Any
from app.services import parser
from app.services import session_manager
from app.services import query_builder
from app.services import db as db_service
from app.models.schemas import AgentResponse


async def handle_message(session_id: str | None, message: str) -> dict[str, Any]:
    """Handle an incoming user message and return agent response.

    Flow:
    - create or load session
    - parse filters from message
    - update conversation state
    - if essentials incomplete -> ask next missing
    - if ready -> build SQL and save to session (do not execute DB here)
    """
    # Create session if needed
    if not session_id:
        session_id = session_manager.create_session()

    state = session_manager.load_conversation_state(session_id)
    if not state:
        # create fresh
        state = state = session_manager.load_conversation_state(session_id)

    # Append user message
    state.messages.append({"role": "user", "content": message})

    # Extract filters from message
    extracted = await parser.parse_filters(message, state.collected_filters)
    if extracted:
        # Merge into collected_filters
        for k, v in extracted.items():
            state.collected_filters[k] = v

    # Determine missing essentials
    essentials = ["distrito", "area_min", "estado", "presupuesto_max", "dormitorios"]
    missing = [f for f in essentials if state.collected_filters.get(f) is None]

    if missing:
        # Ask for the next missing
        next_missing = missing[0]
        # Simple question templates - in future use prompts.system
        question_map = {
            "distrito": "¿En qué distrito te gustaría buscar?",
            "area_min": "¿Cuál es el área mínima que buscas (en m²)?",
            "estado": "¿Qué estado prefieres (DISPONIBLE, OCUPADA, MANTENIMIENTO, VENDIDA)?",
            "presupuesto_max": "¿Cuál es tu presupuesto máximo?",
            "dormitorios": "¿Cuántos dormitorios necesitas?",
        }
        reply = question_map.get(next_missing, "¿Puedes darme más detalles?")
        state.messages.append({"role": "assistant", "content": reply})
        session_manager.save_conversation_state(session_id, state)
        return AgentResponse(session_id=session_id, reply=reply).model_dump()

    # If no missing essentials, proceed to build SQL
    sql, params = query_builder.build_property_search_query(state.collected_filters)

    # Execute query and save results
    try:
        results = await db_service.fetch(sql, *params)
    except Exception as e:
        # Save generated SQL for debugging and return friendly error
        session_manager.save_query_result(session_id, sql, None)
        reply = "Lo siento, hubo un error al ejecutar la búsqueda. Intenta más tarde."
        state.messages.append({"role": "assistant", "content": reply})
        session_manager.save_conversation_state(session_id, state)
        return AgentResponse(session_id=session_id, reply=reply).model_dump()

    # Save results in session
    session_manager.save_query_result(session_id, sql, results)

    reply = f"Encontré {len(results)} propiedades que cumplen con tus criterios. Te las muestro." if results else "Lo siento, no encontré propiedades con esos criterios."
    state.messages.append({"role": "assistant", "content": reply})
    session_manager.save_conversation_state(session_id, state)

    return AgentResponse(session_id=session_id, reply=reply, data=results).model_dump()


async def handle_message(session_id: str | None, message: str) -> dict[str, Any]:
    """Handle an incoming user message and return agent response.

    TODO: implement orchestration logic.
    """
    return {"ok": True, "session_id": session_id, "reply": "placeholder"}
