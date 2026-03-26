import sqlglot
from sqlglot import exp


def validate_select_only(sql: str) -> str:
    statements = sqlglot.parse(sql, dialect="postgres")

    if not statements:
        raise ValueError("Empty SQL statement")

    for statement in statements:
        if statement is None:
            raise ValueError("Failed to parse SQL statement")
        if not isinstance(statement, exp.Select):
            raise ValueError(
                f"Only SELECT queries are allowed. Got: {type(statement).__name__}"
            )

    return sql
