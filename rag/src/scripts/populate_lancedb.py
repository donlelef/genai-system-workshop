"""Populate LanceDB with movie embeddings."""

from langfuse import get_client

from rag.src.infrastructure.data_loader import load_movies
from rag.src.infrastructure.embeddings import embed_texts
from rag.src.infrastructure.lancedb_store import populate
from rag.src.infrastructure.observability import init_observability


def main() -> None:
    init_observability()

    print("Loading movies...")
    movies = load_movies()
    print(f"Loaded {len(movies)} movies.")

    overviews = [m.overview for m in movies]
    print("Generating embeddings (this may take a while)...")
    embeddings = embed_texts(overviews)

    print("Populating LanceDB...")
    populate(movies, embeddings)
    print("Done. LanceDB table created with FTS index.")

    get_client().flush()


if __name__ == "__main__":
    main()
