import logging
import sys

from langfuse import observe

from rag.src.infrastructure.lancedb_store import hybrid_search
from rag.src.infrastructure.llm import generate_answer
from rag.src.scripts import setup_logging

logger = logging.getLogger(__name__)


@observe(name="rag-lancedb-query")
def main() -> None:
    setup_logging()

    if len(sys.argv) < 2:
        logger.error("Usage: query_lancedb.py <question>")
        sys.exit(1)

    question = sys.argv[1]

    logger.info("Question: %s", question)
    results = hybrid_search(query_text=question, limit=10)
    answer = generate_answer(question, results)
    logger.info("Answer:\n%s", answer)


if __name__ == "__main__":
    main()
