import logging

from rag.src.infrastructure.data_loader import load_movies
from rag.src.infrastructure.embeddings import embed_texts
from rag.src.infrastructure.qdrant_store import populate
from rag.src.scripts import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()

    movies = load_movies()

    overviews = [m.overview for m in movies]
    logger.info("Generating embeddings for %d overviews...", len(overviews))
    embeddings = embed_texts(overviews)

    logger.info("Populating Qdrant...")
    populate(movies, embeddings)
    logger.info("Done.")


if __name__ == "__main__":
    main()
