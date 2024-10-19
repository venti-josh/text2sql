import logging

from app.core.ai_models.bedrock import DDL, TABLE_CONTEXT, Model
from app.core.config import settings
from app.core.db import DBClient
from app.core.db import client as db_client
from app.models.query import QueryResponse

logger = logging.getLogger(__name__)


class Text2SQL:
    def __init__(self, db_client: DBClient, *args, **kwargs):
        self._db_client = db_client
        self._model = Model(*args, **kwargs)

    def process_query(self, query: str, retries: int = 3) -> QueryResponse:
        tries = 0
        while tries < retries:
            try:
                sql = self._model.generate_sql(query)
                print(f"SQL: {sql}")
                sql = self._model.validate_sql_query(sql)
                print(f"Validated SQL: {sql}")
                query_explanation = self._model.explain_query(sql)
                print(f"Query Explanation: {sql}")
                results = self._db_client.execute(sql)
                print(f"Results:\n {results[:10]}")
                columns = results[0]
                results = results[1:]
                explanation = self._model.interpret_results(
                    columns, len(results), query
                )
                return QueryResponse(
                    success=True,
                    columns=columns,
                    results=results,
                    explanation=explanation,
                    sql=sql,
                    sql_explanation=query_explanation,
                    query=query,
                )
            except Exception as e:
                logger.exception(f"Try {tries} for query {query} failed", exc_info=e)
                tries += 1
        return QueryResponse(
            success=False,
            columns=[],
            results=[],
            explanation="Failed to generate results for the query. Please try a different question.",
            sql_explanation="",
            query=query,
            sql="",
        )


# client = Text2SQL(
#     config={
#         "api_key": settings.OPENAI_API_KEY,
#         "model": settings.OPENAI_MODEL,
#         "path": settings.CHROMA_DB_PATH,
#         "client": "persistent",
#     }
# )

client = Text2SQL(
    db_client=db_client,
    aws_credentials={
        "AWS_REGION": settings.AWS_REGION,
        "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY,
    },
    ddl=DDL,
    table_context=TABLE_CONTEXT,
)
