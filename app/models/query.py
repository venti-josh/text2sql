from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    columns: list[str]
    results: list[Any]
    query: str
    sql: str
    sql_explanation: str
    explanation: str
    success: bool
