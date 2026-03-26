from pydantic import BaseModel, Field


class TableInfo(BaseModel):
    name: str = Field(description="Table name")
    description: str = Field(description="Short description of the table")


class ColumnInfo(BaseModel):
    name: str = Field(description="Column name")
    data_type: str = Field(description="SQL data type")
    description: str = Field(description="Short description of the column")


class TableSchema(BaseModel):
    table_name: str = Field(description="Table name")
    columns: list[ColumnInfo] = Field(description="Column definitions")
    sample_values: dict[str, list[str]] = Field(
        description="Sample values per column (column_name -> list of example values)"
    )


class QueryResult(BaseModel):
    columns: list[str] = Field(description="Column names in the result set")
    rows: list[list[str]] = Field(description="Result rows, each cell as a string")
