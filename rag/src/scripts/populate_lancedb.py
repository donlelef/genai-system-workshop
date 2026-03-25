import logging

from rag.src.infrastructure.data_loader import load_movies
from rag.src.infrastructure.lancedb_store import populate
from rag.src.scripts import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()

    movies = load_movies()

    logger.info("Populating LanceDB (embeddings generated automatically)...")
    populate(movies)
    logger.info("Done.")


if __name__ == "__main__":
    main()
