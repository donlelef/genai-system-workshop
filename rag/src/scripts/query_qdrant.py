import logging
import sys

from langfuse import get_client, observe, propagate_attributes

from infrastructure.embeddings import embed_single
from infrastructure.llm import generate_answer, generate_hypothetical_document
from infrastructure.qdrant_store import vector_search
from scripts import setup_logging

logger = logging.getLogger(__name__)


@observe(name="rag-qdrant-query")
def run_query(question: str) -> str:
    with propagate_attributes(tags=["rag", "qdrant", "hyde"]):
        logger.info("Question: %s", question)
        hypothetical_overview = generate_hypothetical_document(question)
        query_vector = embed_single(hypothetical_overview)
        results = vector_search(query_vector=query_vector, limit=10)
        answer = generate_answer(question, results)
        logger.info("Answer:\n%s", answer)
        return answer


def main() -> None:
    setup_logging()

    if len(sys.argv) < 2:
        logger.error("Usage: query_qdrant.py <question>")
        sys.exit(1)

    run_query(sys.argv[1])
    get_client().flush()


if __name__ == "__main__":
    main()
