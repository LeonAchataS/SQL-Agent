"""Pydantic V2 schemas for agent inputs/outputs and filter models.

Define FilterEssential, FilterOptional, AgentMessage, AgentResponse, etc.
"""

from pydantic import BaseModel
from typing import Optional


class FilterEssential(BaseModel):
    distrito: str
    area_min: Optional[float]
    estado: Optional[str]
    presupuesto_max: Optional[float]
    dormitorios: Optional[int]


class FilterOptional(BaseModel):
    pet_friendly: Optional[bool]
    balcon: Optional[bool]
    terraza: Optional[bool]
    amoblado: Optional[bool]
    banios: Optional[int]


class AgentMessage(BaseModel):
    session_id: Optional[str]
    message: str


class AgentResponse(BaseModel):
    session_id: Optional[str]
    reply: str
    data: Optional[list] = None
