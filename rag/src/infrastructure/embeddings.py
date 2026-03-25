from langfuse.openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts using OpenAI embeddings."""
    response = _get_client().embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_single(text: str) -> list[float]:
    """Embed a single text string."""
    return embed_texts([text])[0]
