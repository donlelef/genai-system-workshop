from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    id: str
    title: str
    overview: str
    release_date: str
    runtime: int
    genre: str


@dataclass(frozen=True)
class SearchResult:
    movie: Movie
    score: float
