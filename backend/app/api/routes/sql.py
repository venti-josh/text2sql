from fastapi import APIRouter, HTTPException

from app.core.text2sql import client
from app.models.query import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    query = request.query

    try:
        response = client.process_query(query)
        if response["status"] == "success":
            return QueryResponse(processed_result=response["sql_query"])
        else:
            raise HTTPException(
                status_code=500, detail=f"Error processing query: {response['message']}"
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
