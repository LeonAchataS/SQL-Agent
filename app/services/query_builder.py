"""Query builder (skeleton): build parameterized SELECT queries from filters.

This module must ensure only SELECT queries are produced and use parameter
placeholders compatible with asyncpg ($1, $2...).
"""

from typing import Any, Tuple


def build_property_search_query(filters: dict) -> Tuple[str, Tuple[Any, ...]]:
    """Return (sql, params) for given filters.

    TODO: implement safe builder and allowlist of columns.
    """
    # Explicit column list to match PropertyResponse schema
    columns = [
        "p.id",
        "p.numero",
        "p.piso",
        "p.tipo",
        "p.area",
        "p.dormitorios",
        "p.banios",
        "p.balcon",
        "p.terraza",
        "p.amoblado",
        "p.permite_mascotas",
        "p.valor_comercial",
        "p.mantenimiento_mensual",
        "p.estado",
        "e.nombre as edificio_nombre",
        "e.direccion as edificio_direccion",
        "e.distrito as edificio_distrito",
    ]

    where_clauses: list[str] = []
    params: list[Any] = []

    def add_param(value: Any) -> str:
        params.append(value)
        return f"${len(params)}"

    # Filter mappings - expect internal keys (presupuesto_max, area_min, distrito, estado, dormitorios)
    if filters.get("distrito"):
        where_clauses.append(f"e.distrito = {add_param(filters['distrito'])}")
    if filters.get("area_min") is not None:
        where_clauses.append(f"p.area >= {add_param(filters['area_min'])}")
    if filters.get("estado"):
        where_clauses.append(f"p.estado = {add_param(filters['estado'])}")
    if filters.get("presupuesto_max") is not None:
        # valor_comercial in DB
        where_clauses.append(f"p.valor_comercial <= {add_param(filters['presupuesto_max'])}")
    if filters.get("dormitorios") is not None:
        where_clauses.append(f"p.dormitorios = {add_param(filters['dormitorios'])}")

    # Optional boolean filters
    if filters.get("pet_friendly") is not None:
        where_clauses.append(f"p.permite_mascotas = {add_param(filters['pet_friendly'])}")
    if filters.get("balcon") is not None:
        where_clauses.append(f"p.balcon = {add_param(filters['balcon'])}")
    if filters.get("terraza") is not None:
        where_clauses.append(f"p.terraza = {add_param(filters['terraza'])}")
    if filters.get("amoblado") is not None:
        where_clauses.append(f"p.amoblado = {add_param(filters['amoblado'])}")
    if filters.get("banios") is not None:
        where_clauses.append(f"p.banios = {add_param(filters['banios'])}")

    where_sql = "\n    AND ".join(where_clauses) if where_clauses else "1=1"

    sql = f"SELECT\n    {', '.join(columns)}\nFROM property_infrastructure.propiedad p\nJOIN property_infrastructure.edificio e ON p.edificio_id = e.id\nWHERE\n    {where_sql}\nORDER BY p.valor_comercial DESC\nLIMIT 5;"

    return sql, tuple(params)
