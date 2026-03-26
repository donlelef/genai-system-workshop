import logging

from infrastructure.data_loader import load_movies
from infrastructure.lancedb_store import populate
from scripts import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()

    movies = load_movies()

    logger.info("Populating LanceDB (embeddings generated automatically)...")
    populate(movies)
    logger.info("Done.")


if __name__ == "__main__":
    main()
