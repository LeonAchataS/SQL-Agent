# SQL Agent - Project skeleton for Custom Agent

This file documents the skeleton added to the repository to implement the
custom agent (parser + query builder + session manager) approach.

Next steps:
- Implement `app.services.llm_client` to call OpenAI and return structured JSON.
- Implement `app.services.parser` to validate and merge extractions into models.
- Implement `app.services.query_builder` to produce parameterized SQL ($1, $2...).
- Implement `app.services.db` with asyncpg pool and safe fetch helpers.
- Wire `app.api.v1.agent_router` to call `app.services.agent_service.handle_message`.
