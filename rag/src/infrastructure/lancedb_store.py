from pathlib import Path

import lancedb
from langfuse import observe

from rag.src.core.models import Movie, SearchResult

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "lancedb"
TABLE_NAME = "movies"


def _connect() -> lancedb.DBConnection:
    return lancedb.connect(str(DB_PATH))


def populate(movies: list[Movie], embeddings: list[list[float]]) -> None:
    """Create or overwrite the LanceDB table with movie data and embeddings."""
    records = [
        {
            "id": m.id,
            "title": m.title,
            "overview": m.overview,
            "release_date": m.release_date,
            "runtime": m.runtime,
            "genre": m.genre,
            "vector": emb,
        }
        for m, emb in zip(movies, embeddings)
    ]

    db = _connect()
    table = db.create_table(TABLE_NAME, data=records, mode="overwrite")
    table.create_fts_index("overview", replace=True)


@observe(name="lancedb-hybrid-search")
def hybrid_search(
    query_text: str,
    query_vector: list[float],
    limit: int = 10,
) -> list[SearchResult]:
    """Hybrid search: combine vector similarity with full-text BM25 on overview."""
    db = _connect()
    table = db.open_table(TABLE_NAME)

    rows = (
        table.search(query_text, query_type="hybrid")
        .vector(query_vector)
        .limit(limit)
        .to_pandas()
    )

    results: list[SearchResult] = []
    for _, row in rows.iterrows():
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
