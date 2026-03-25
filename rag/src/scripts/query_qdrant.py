"""Query Qdrant using HyDE + vector search."""

import sys

from langfuse import get_client, observe

from rag.src.infrastructure.embeddings import embed_single
from rag.src.infrastructure.llm import generate_answer, generate_hypothetical_document
from rag.src.infrastructure.observability import init_observability
from rag.src.infrastructure.qdrant_store import vector_search


@observe(name="rag-qdrant-query")
def run_query(question: str) -> str:
    hypothetical_overview = generate_hypothetical_document(question)
    query_vector = embed_single(hypothetical_overview)
    results = vector_search(query_vector=query_vector, limit=10)
    return generate_answer(question, results)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: query_qdrant.py <question>")
        sys.exit(1)

    init_observability()
    question = sys.argv[1]

    print(f"Question: {question}\n")
    answer = run_query(question)
    print(f"Answer:\n{answer}")

    get_client().flush()


if __name__ == "__main__":
    main()
