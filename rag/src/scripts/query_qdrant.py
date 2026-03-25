import logging
import sys

from langfuse import observe

from rag.src.infrastructure.embeddings import embed_single
from rag.src.infrastructure.llm import generate_answer, generate_hypothetical_document
from rag.src.infrastructure.qdrant_store import vector_search
from rag.src.scripts import setup_logging

logger = logging.getLogger(__name__)


@observe(name="rag-qdrant-query")
def main() -> None:
    setup_logging()

    if len(sys.argv) < 2:
        logger.error("Usage: query_qdrant.py <question>")
        sys.exit(1)

    question = sys.argv[1]

    logger.info("Question: %s", question)
    hypothetical_overview = generate_hypothetical_document(question)
    query_vector = embed_single(hypothetical_overview)
    results = vector_search(query_vector=query_vector, limit=10)
    answer = generate_answer(question, results)
    logger.info("Answer:\n%s", answer)


if __name__ == "__main__":
    main()
