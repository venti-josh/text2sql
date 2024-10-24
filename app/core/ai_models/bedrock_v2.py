import json
import logging
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import boto3

logger = logging.getLogger(__name__)


class Model:
    def __init__(self, aws_credentials):
        self.aws_credentials = aws_credentials
        self.schema_data = self._load_schema(
            str(Path(__file__).parent.joinpath("Comprehensive Tables.json").absolute())
        )
        self.table_column_map = self._build_table_column_map()
        self.bedrock_client = self._initialize_bedrock_client()
        self.model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def _load_schema(self, file: str) -> dict[str, Any]:
        try:
            with open(file) as f:
                schema_data = json.load(f)
            return schema_data
        except Exception as e:
            logger.error(f"Error loading schema file: {e}")
            return {}

    def _initialize_bedrock_client(self):
        return boto3.client(
            "bedrock-runtime",
            region_name=self.aws_credentials["AWS_REGION"],
            aws_access_key_id=self.aws_credentials["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=self.aws_credentials["AWS_SECRET_ACCESS_KEY"],
        )

    def _build_table_column_map(self) -> dict:
        table_map = {}
        for table_name, table_info in self.schema_data.items():
            table_map[table_name] = {
                "columns": {col["name"]: col for col in table_info.get("columns", [])},
                "description": table_info.get("table_description", ""),
            }
        return table_map

    def invoke_bedrock_model(self, prompt: str) -> str:
        try:
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1024,
                        "messages": [{"role": "user", "content": prompt}],
                    }
                ),
            )

            resp = json.loads(response["body"].read())
            return resp["content"][0]["text"].strip()
        except Exception as e:
            logger.error(f"An error occurred during model invocation: {e}")
            return ""  # Return empty string instead of None

    def generate_sql(self, query: str) -> str:
        # Create a formatted schema string from the JSON data
        schema_info = []
        for table_name, table_data in self.schema_data.items():
            schema_info.append(f"Table: {table_name}")
            schema_info.append(
                f"Description: {table_data.get('table_description', '')}"
            )
            schema_info.append("Columns:")
            for column in table_data.get("columns", []):
                schema_info.append(
                    f"  - {column['name']} ({column['type']}): {column.get('description', '')}"
                )
            schema_info.append("n")

        prompt = f"""Generate a SQL query for the following question:

User Query: {query}

Schema Information:
{'n'.join(schema_info)}

Provide only the SQL query without any explanation or comments.
Enclose the SQL query in triple backticks with the sql tag, like this:
```sql
YOUR SQL QUERY HERE
```
"""

        response = self.invoke_bedrock_model(prompt)
        # Extract the SQL query from the response
        sql_pattern = r"```sql\n(.*?)\n```"
        match = re.search(sql_pattern, response, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response.strip()

    def explain_query(self, sql_query: str) -> str:
        prompt = f"""Briefly explain the following SQL query in one or two sentences:

SQL Query:
{sql_query}
"""

        explanation = self.invoke_bedrock_model(prompt)
        return explanation

    def validate_sql_query(self, sql_query: str) -> str:
        # Extract table aliases from the query
        table_aliases = {}
        for match in re.finditer(
            r"FROMs+(\w+)\s+(?:AS\s+)?(\w+)|JOIN\s+(\w+)\s+(?:AS\s+)?(\w+)",
            sql_query,
            re.IGNORECASE,
        ):
            if match.group(1) and match.group(2):  # FROM clause
                table_aliases[match.group(2)] = match.group(1)
            elif match.group(3) and match.group(4):  # JOIN clause
                table_aliases[match.group(4)] = match.group(3)

        # Validate tables
        invalid_tables = []
        for table_name in table_aliases.values():
            if table_name not in self.table_column_map:
                invalid_tables.append(table_name)

        # Extract and validate columns
        invalid_columns = []
        for match in re.finditer(
            r"(?:SELECT|WHERE|GROUP BY|ORDER BY)\s+(.*?)(?:FROM|WHERE|GROUP BY|ORDER BY|$)",
            sql_query,
            re.IGNORECASE,
        ):
            columns_section = match.group(1)
            for col_ref in re.finditer(r"(\w+)\.(\w+)", columns_section):
                alias, column = col_ref.groups()
                if alias in table_aliases:
                    table_name = table_aliases[alias]
                    if column not in self.table_column_map[table_name]["columns"]:
                        invalid_columns.append(f"{column} in table {table_name}")

        if invalid_tables or invalid_columns:
            correction_prompt = f"""
The SQL query has validation errors:
{sql_query}

Issues found:
{"Invalid tables: " + ", ".join(invalid_tables) if invalid_tables else ""}
{"Invalid columns: " + ", ".join(invalid_columns) if invalid_columns else ""}

Valid tables and their columns are:
"""
            # Add relevant table information
            for table_name, table_info in self.table_column_map.items():
                if any(table_name.lower() in col.lower() for col in invalid_columns):
                    correction_prompt += f"\nTable: {table_name}\n"
                    correction_prompt += f"Description: {table_info['description']}\n"
                    correction_prompt += "Columns:\n"
                    for col_name in table_info["columns"].keys():
                        correction_prompt += f"  - {col_name}\n"

            correction_prompt += (
                "\nPlease correct the query using only valid tables and columns."
            )

            return self.invoke_bedrock_model(correction_prompt)

        return sql_query

    def interpret_results(
        self, columns: Iterable[str], num_rows: int, original_query: str
    ) -> str:
        prompt = f"""Given the following query and result summary, provide a brief, two-line interpretation:

Original query: {original_query}

Result summary:
Number of rows: {num_rows}
Columns: {', '.join(columns)}

Interpret the results in two lines or less, directly answering the original query.
"""

        interpretation = self.invoke_bedrock_model(prompt)
        return interpretation
