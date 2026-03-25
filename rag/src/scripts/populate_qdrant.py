"""Populate Qdrant with movie embeddings."""

from langfuse import get_client

from rag.src.infrastructure.data_loader import load_movies
from rag.src.infrastructure.embeddings import embed_texts
from rag.src.infrastructure.observability import init_observability
from rag.src.infrastructure.qdrant_store import populate


def main() -> None:
    init_observability()

    print("Loading movies...")
    movies = load_movies()
    print(f"Loaded {len(movies)} movies.")

    overviews = [m.overview for m in movies]
    print("Generating embeddings (this may take a while)...")
    embeddings = embed_texts(overviews)

    print("Populating Qdrant...")
    populate(movies, embeddings)
    print("Done. Qdrant collection created.")

    get_client().flush()


if __name__ == "__main__":
    main()
