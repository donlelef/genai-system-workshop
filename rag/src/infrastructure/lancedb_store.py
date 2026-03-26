import logging
from pathlib import Path

import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from langfuse import observe

from core.models import Movie, SearchResult

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "lancedb"
TABLE_NAME = "movies"

_embedding = get_registry().get("openai").create(name="text-embedding-3-small")


class MovieRecord(LanceModel):
    id: str
    title: str
    overview: str = _embedding.SourceField()
    release_date: str
    runtime: int
    genre: str
    vector: Vector(_embedding.ndims()) = _embedding.VectorField()


def _connect() -> lancedb.DBConnection:
    return lancedb.connect(str(DB_PATH))


BATCH_SIZE = 2048


def populate(movies: list[Movie]) -> None:
    records = [
        {
            "id": m.id,
            "title": m.title,
            "overview": m.overview,
            "release_date": m.release_date,
            "runtime": m.runtime,
            "genre": m.genre,
        }
        for m in movies
    ]

    db = _connect()
    table = db.create_table(TABLE_NAME, schema=MovieRecord, mode="overwrite")

    for i in range(0, len(records), BATCH_SIZE):
        batch = records[i : i + BATCH_SIZE]
        table.add(batch)
        logger.info(
            "Embedded batch %d/%d", i // BATCH_SIZE + 1, -(-len(records) // BATCH_SIZE)
        )

    table.create_fts_index("overview", replace=True)


@observe(name="lancedb-hybrid-search")
def hybrid_search(
    query_text: str,
    limit: int = 10,
) -> list[SearchResult]:
    db = _connect()
    table = db.open_table(TABLE_NAME)

    rows = table.search(query_text, query_type="hybrid").limit(limit).to_list()

    results: list[SearchResult] = []
    for row in rows:
        movie = Movie(
            id=str(row["id"]),
            title=str(row["title"]),
            overview=str(row["overview"]),
            release_date=str(row["release_date"]),
            runtime=int(row["runtime"]),
            genre=str(row["genre"]),
        )
        results.append(SearchResult(movie=movie, score=float(row.get("_score", 0.0))))
    return results
