from datetime import datetime
from typing import Any, Union, get_type_hints
from app.models.query import QueryRequest, QueryResponse
from pydantic import BaseModel, Field
from app.core.openai import client
from fastapi import HTTPException, APIRouter


# Function to convert Python types to SQL-like types, with handling for more complex types
def python_type_to_sql_type(python_type):
    if hasattr(
        python_type, "__origin__"
    ):  # Handle complex types like Optional, List, etc.
        origin = python_type.__origin__
        args = python_type.__args__

        if origin is Union and type(None) in args:  # Optional field
            non_optional_type = [arg for arg in args if arg is not type(None)][0]
            return f"{python_type_to_sql_type(non_optional_type)} (NULL)"
        elif origin is list:  # Lists can represent arrays or foreign key relationships
            return f"ARRAY[{python_type_to_sql_type(args[0])}]"
        elif origin is dict:  # Handling for Dict types
            return "JSON"

    # Handle standard types, including Enums and custom types
    type_mapping = {
        int: "INTEGER",
        float: "FLOAT",
        str: "STRING",
        datetime: "DATETIME",
    }
    return type_mapping.get(python_type, "UNKNOWN")


# Function to generate schema from Pydantic model with handling for complex types
def generate_table_schema(model: BaseModel) -> str:
    schema = f"**{model.__name__} table**\n"
    fields = get_type_hints(model)

    for field_name, field_type in fields.items():
        sql_type = python_type_to_sql_type(field_type)
        schema += f"- {field_name} ({sql_type})\n"
    return schema

class SQLResponse(BaseModel):
    sql_query: str = Field(..., description="The generated SQL query")
    explanation: str = Field(..., description="A brief explanation of the SQL query and how it addresses the user's question")
    used_tables: list[str] = Field(..., description="List of tables used in the query")
    used_columns: list[str] = Field(..., description="List of columns used in the query")

class TextToSQl:
    QUERY_TEMPLATE = """As an expert SQL query generator, convert the following natural language query into a SQL query based on the given dataset metadata. Consider multiple tables and their relationships.

Dataset Metadata:
{metadata}

User Query: {query}

Generate a SQL query that answers the user's question, using proper JOINs if necessary.
Provide a brief explanation of the generated SQL query.

Your response should be a JSON object with the following structure:
{
    "sql_query": "The generated SQL query",
    "explanation": "A brief explanation of the SQL query and how it addresses the user's question",
    "used_tables": ["List of tables used in the query"],
    "used_columns": ["List of columns used in the query"]
}
"""

    @classmethod
    async def process_query(cls, query: str, models: list[BaseModel]) -> dict[str, Any]:
        prompt = cls.QUERY_TEMPLATE.format(
            metadata="\n".join([generate_table_schema(model) for model in models]),
            query=query,
        )
        try:
            completion = await client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in converting natural language queries to SQL for complex, multi-table datasets."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
            )

            response_content = completion.choices[0].message.content
            result = SQLResponse.model_validate_json(response_content)

            return {
                "status": "success",
                "original_query": query,
                "sql_query": result.sql_query,
                "explanation": result.explanation,
                "used_tables": result.used_tables,
                "used_columns": result.used_columns,
            }
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                "status": "error",
                "original_query": query,
                "message": f"An error occurred: {str(e)}. Please try again.",
            }

router = APIRouter()

@router.post("/query/", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    query = request.query

    try:
        # Send the query to the OpenAI API
        response = TextToSQl.process_query(query, models=[])

        # Process the result (for now, just take the first response)
        processed_result = response.choices[0].text.strip()

        # Return the processed result
        return QueryResponse(processed_result=processed_result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# Note: The `generate_table_schema` function and `models` list are not defined in this file.
# They should be imported or defined elsewhere in your application.
