import logging
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from sqlalchemy import text

from core.catalog import get_schema, get_table_list
from core.models import QueryResult, TableInfo, TableSchema
from infrastructure.database import get_engine
from infrastructure.logging_config import setup_logging
from infrastructure.sql_validator import validate_select_only

logger = logging.getLogger(__name__)

mcp = FastMCP(name="DatabaseServer")


@mcp.tool()
def get_tables() -> list[TableInfo]:
    """Return every table in the database with a short description."""
    logger.info("get_tables called")
    return get_table_list()


@mcp.tool()
def get_table_schema(
    table_name: Annotated[str, Field(description="Name of the table to describe")],
) -> TableSchema:
    """Return column definitions and sample values for the given table."""
    logger.info("get_table_schema called for %s", table_name)
    return get_schema(table_name)


@mcp.tool()
def run_sql(
    query: Annotated[str, Field(description="A PostgreSQL SELECT query to execute")],
) -> QueryResult:
    """Validate and execute a read-only SQL query, returning the result set."""
    logger.info("run_sql called: %s", query)
    validate_select_only(query)

    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        columns = list(result.keys())
        rows = [[str(cell) for cell in row] for row in result.fetchall()]

    logger.info("Query returned %d rows", len(rows))
    return QueryResult(columns=columns, rows=rows)


if __name__ == "__main__":
    setup_logging()
    logger.info("Starting Database MCP server on 127.0.0.1:8000")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
