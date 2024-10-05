from datetime import datetime
from typing import Union, get_type_hints

from pydantic import BaseModel


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
