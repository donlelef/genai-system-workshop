"""Query LanceDB using HyDE + hybrid search."""

import sys

from langfuse import get_client, observe

from rag.src.infrastructure.embeddings import embed_single
from rag.src.infrastructure.lancedb_store import hybrid_search
from rag.src.infrastructure.llm import generate_answer, generate_hypothetical_document
from rag.src.infrastructure.observability import init_observability


@observe(name="rag-lancedb-query")
def run_query(question: str) -> str:
    hypothetical_overview = generate_hypothetical_document(question)
    query_vector = embed_single(hypothetical_overview)
    results = hybrid_search(
        query_text=question,
        query_vector=query_vector,
        limit=10,
    )
    return generate_answer(question, results)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: query_lancedb.py <question>")
        sys.exit(1)

    init_observability()
    question = sys.argv[1]

    print(f"Question: {question}\n")
    answer = run_query(question)
    print(f"Answer:\n{answer}")

    get_client().flush()


if __name__ == "__main__":
    main()
