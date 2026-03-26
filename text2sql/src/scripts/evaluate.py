import json
import logging
from pathlib import Path

from openai import OpenAI
from sqlalchemy import text

from core.catalog import get_schema, get_table_list
from core.prompts import EVALUATION_SQL_PROMPT
from infrastructure.database import get_engine
from infrastructure.logging_config import setup_logging
from infrastructure.sql_validator import validate_select_only

logger = logging.getLogger(__name__)

DATASET_PATH = Path(__file__).resolve().parent.parent / "evaluation" / "dataset.json"
CHAT_MODEL = "gpt-5.4"


def _build_schema_context() -> str:
    parts: list[str] = []
    for table_info in get_table_list():
        schema = get_schema(table_info.name)
        cols = "\n".join(
            f"  - {c.name} ({c.data_type}): {c.description}" for c in schema.columns
        )
        samples = "\n".join(
            f"  - {col}: {vals}" for col, vals in schema.sample_values.items()
        )
        parts.append(
            f"Table: {schema.table_name}\n"
            f"Description: {table_info.description}\n"
            f"Columns:\n{cols}\n"
            f"Sample values:\n{samples}"
        )
    return "\n\n".join(parts)


def _generate_sql(question: str, schema_context: str) -> str:
    client = OpenAI()
    prompt = EVALUATION_SQL_PROMPT.format(
        schema_context=schema_context, question=question
    )
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions="You are an expert SQL assistant.",
        input=prompt,
        temperature=0.0,
        store=False,
    )
    return (response.output_text or "").strip()


def _execute_query(query: str) -> list[tuple[str, ...]]:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(query))
        return [tuple(str(cell) for cell in row) for row in result.fetchall()]


def _results_match(
    actual: list[tuple[str, ...]], expected: list[tuple[str, ...]]
) -> bool:
    return sorted(actual) == sorted(expected)


def _load_dataset() -> list[dict[str, str]]:
    return json.loads(DATASET_PATH.read_text())


def main() -> None:
    setup_logging()

    dataset = _load_dataset()
    schema_context = _build_schema_context()
    passed = 0

    for i, item in enumerate(dataset, start=1):
        question = item["question"]
        ground_truth_sql = item["ground_truth_sql"]
        logger.info("--- [%d/%d] %s", i, len(dataset), question)

        try:
            generated_sql = _generate_sql(question, schema_context)
            logger.info("Generated SQL: %s", generated_sql)
            validate_select_only(generated_sql)
        except Exception:
            logger.exception("SQL generation or validation failed")
            continue

        try:
            expected_rows = _execute_query(ground_truth_sql)
            actual_rows = _execute_query(generated_sql)
        except Exception:
            logger.exception("Query execution failed")
            continue

        if _results_match(actual_rows, expected_rows):
            passed += 1
            logger.info("PASS")
        else:
            logger.warning(
                "FAIL — expected %d rows, got %d", len(expected_rows), len(actual_rows)
            )
            logger.warning("  Expected: %s", expected_rows[:3])
            logger.warning("  Actual:   %s", actual_rows[:3])

    logger.info(
        "=== Results: %d/%d passed (%.0f%%) ===",
        passed,
        len(dataset),
        100 * passed / len(dataset),
    )


if __name__ == "__main__":
    main()
