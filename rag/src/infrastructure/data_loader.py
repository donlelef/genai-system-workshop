from pathlib import Path

import pandas as pd

from rag.src.core.models import Movie

DATA_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "movies.parquet"


def load_movies() -> list[Movie]:
    """Load movies from the parquet file into domain objects."""
    df = pd.read_parquet(DATA_PATH)
    return [
        Movie(
            id=str(row["id"]),
            title=str(row["title"]),
            overview=str(row["overview"]),
            release_date=str(row["release_date"]),
            runtime=int(row["runtime"]),
            genre=str(row["genre"]),
        )
        for _, row in df.iterrows()
    ]
