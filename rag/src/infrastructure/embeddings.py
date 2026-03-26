import logging

from langfuse import observe
from langfuse.openai import OpenAI

logger = logging.getLogger(__name__)

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536
BATCH_SIZE = 2048


@observe(name="embed-texts")
def embed_texts(texts: list[str]) -> list[list[float]]:
    client = OpenAI()
    all_embeddings: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        all_embeddings.extend(item.embedding for item in response.data)
        logger.info(
            "Embedded batch %d/%d", i // BATCH_SIZE + 1, -(-len(texts) // BATCH_SIZE)
        )

    return all_embeddings


@observe(name="embed-single")
def embed_single(text: str) -> list[float]:
    return embed_texts([text])[0]
