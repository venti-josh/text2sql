from fastapi import APIRouter, HTTPException

from app.core.text2sql import client as text2sql_client
from app.models.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    query = request.query

    try:
        response = text2sql_client.process_query(query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
