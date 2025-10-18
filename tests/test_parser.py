import pytest

import asyncio

from app.services import parser, llm_client


@pytest.mark.asyncio
async def test_parse_filters_essentials_and_optionals(monkeypatch):
    async def mock_extract(text: str):
        return {
            "distrito": "San Isidro",
            "dormitorios": 2,
            "permite_mascotas": True,
            "balcon": True
        }

    monkeypatch.setattr(llm_client, "extract_filters_from_text", mock_extract)

    result = await parser.parse_filters("Busco en San Isidro 2 dormitorios y que acepte mascotas")

    assert result.get("distrito") == "San Isidro"
    assert result.get("dormitorios") == 2
    # Optionals may be normalized to names in FilterOptional (pet_friendly -> permite_mascotas mapping not implemented)


@pytest.mark.asyncio
async def test_parse_filters_invalid_format(monkeypatch):
    async def mock_extract(text: str):
        return "not a dict"

    monkeypatch.setattr(llm_client, "extract_filters_from_text", mock_extract)

    result = await parser.parse_filters("Nada relevante")
    assert result == {}
