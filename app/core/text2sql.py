from typing import Any

from pydantic import BaseModel, Field
from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat

from app.core.config import settings
from app.core.openai import client as openai_client
from app.core.utils import generate_table_schema


class Model(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)


class SQLResponse(BaseModel):
    sql_query: str = Field(..., description="The generated SQL query")
    explanation: str = Field(
        ...,
        description="A brief explanation of the SQL query and how it addresses the user's question",
    )
    used_tables: list[str] = Field(..., description="List of tables used in the query")
    used_columns: list[str] = Field(
        ..., description="List of columns used in the query"
    )


class Text2SQL:
    def __init__(self, config=None):
        self.model = Model(config=config)

    def process_query(self, query: str, retries: int = 3) -> dict[str, Any]:
        tries = 0
        while tries < retries:
            sql = self.model.generate_sql(query)
            is_valid = self.model.is_sql_valid(sql)
            if is_valid:
                return {
                    "status": "success",
                    "original_query": query,
                    "sql_query": sql,
                }
            tries += 1
        return {
            "status": "error",
            "original_query": query,
            "message": "Failed to generate a valid SQL query.",
        }

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
    async def process_query_with_models(
        cls, query: str, models: list[BaseModel]
    ) -> dict[str, Any]:
        prompt = cls.QUERY_TEMPLATE.format(
            metadata="\n".join([generate_table_schema(model) for model in models]),
            query=query,
        )
        try:
            completion = await openai_client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant specialized in converting natural language queries to SQL for complex, multi-table datasets.",
                    },
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


client = Text2SQL(
    config={
        "api_key": settings.OPENAI_API_KEY,
        "model": settings.OPENAI_MODEL,
        "path": settings.CHROMA_DB_PATH,
        "client": "persistent",
    }
)
