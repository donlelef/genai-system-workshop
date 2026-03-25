import os

from langfuse import observe
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from rag.src.core.models import Movie, SearchResult
from rag.src.infrastructure.embeddings import EMBEDDING_DIMENSIONS

COLLECTION_NAME = "movies"


def _connect() -> QdrantClient:
    url = os.environ.get("QDRANT_URL", "http://localhost:6333")
    return QdrantClient(url=url)


def populate(movies: list[Movie], embeddings: list[list[float]]) -> None:
    """Create or recreate the Qdrant collection with movie data and embeddings."""
    client = _connect()

    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=EMBEDDING_DIMENSIONS,
            distance=Distance.COSINE,
        ),
    )

    points = [
        PointStruct(
            id=idx,
            vector=emb,
            payload={
                "id": m.id,
                "title": m.title,
                "overview": m.overview,
                "release_date": m.release_date,
                "runtime": m.runtime,
                "genre": m.genre,
            },
        )
        for idx, (m, emb) in enumerate(zip(movies, embeddings))
    ]

    batch_size = 100
    for i in range(0, len(points), batch_size):
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points[i : i + batch_size],
        )


@observe(name="qdrant-vector-search")
def vector_search(
    query_vector: list[float],
    limit: int = 10,
) -> list[SearchResult]:
    """Pure cosine vector search against Qdrant."""
    client = _connect()

    hits = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
    ).points

    results: list[SearchResult] = []
    for hit in hits:
        p = hit.payload or {}
        movie = Movie(
            id=str(p["id"]),
            title=str(p["title"]),
            overview=str(p["overview"]),
            release_date=str(p["release_date"]),
            runtime=int(p["runtime"]),
            genre=str(p["genre"]),
        )
        results.append(SearchResult(movie=movie, score=float(hit.score)))
    return results
