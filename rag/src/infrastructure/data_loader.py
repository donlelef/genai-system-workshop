from pathlib import Path

import polars as pl

from rag.src.core.models import Movie

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "movies.parquet"


def load_movies() -> list[Movie]:
    df = pl.read_parquet(DATA_PATH)
    return [
        Movie(
            id=str(row["id"]),
            title=str(row["title"]),
            overview=str(row["overview"]),
            release_date=str(row["release_date"]),
            runtime=int(row["runtime"]),
            genre=str(row["genre"]),
        )
        for row in df.iter_rows(named=True)
    ]
