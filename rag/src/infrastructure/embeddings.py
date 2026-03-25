from langfuse.openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = OpenAI()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def embed_single(text: str) -> list[float]:
    return embed_texts([text])[0]
