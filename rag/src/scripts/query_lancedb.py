import logging
import sys

from langfuse import get_client, observe, propagate_attributes

from infrastructure.lancedb_store import hybrid_search
from infrastructure.llm import generate_answer
from scripts import setup_logging

logger = logging.getLogger(__name__)


@observe(name="rag-lancedb-query")
def run_query(question: str) -> str:
    with propagate_attributes(tags=["rag", "lancedb"]):
        logger.info("Question: %s", question)
        results = hybrid_search(query_text=question)
        answer = generate_answer(question, results)
        logger.info("Answer:\n%s", answer)
        return answer


def main() -> None:
    setup_logging()

    if len(sys.argv) < 2:
        logger.error("Usage: query_lancedb.py <question>")
        sys.exit(1)

    run_query(sys.argv[1])
    get_client().flush()


if __name__ == "__main__":
    main()
