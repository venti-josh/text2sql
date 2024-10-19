from collections.abc import Iterable
from typing import Any

import pandas as pd
import pyodbc

from app.core.config import settings

DRIVER = "{ODBC Driver 17 for SQL Server}"


class DBClient:
    def __init__(self) -> None:
        self._connection_string = (
            f"DRIVER={DRIVER};"
            f"SERVER={settings.DB_SERVER};"
            f"DATABASE={settings.DB_DATABASE};"
            f"UID={settings.DB_USER};"
            f"PWD={settings.DB_PASSWORD};"
        )
        self._conn = pyodbc.connect(self._connection_string, readonly=True, timeout=60)

    def execute(self, query: str) -> Iterable[tuple[Any]]:
        result = pd.read_sql_query(query, self._conn)
        return [result.columns.tolist()] + result.values.tolist()
        # with self._conn.cursor() as cursor:
        #     cursor.execute(query)
        #     columns = cursor.description
        #     return [(column[0] for column in columns)] + cursor.fetchall()


client = DBClient()
