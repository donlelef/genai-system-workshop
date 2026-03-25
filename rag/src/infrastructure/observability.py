from langfuse import Langfuse

_client: Langfuse | None = None


def init_observability() -> Langfuse:
    """Initialize and return the Langfuse singleton client.

    Expects LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY, and LANGFUSE_BASE_URL
    to already be set as environment variables (injected via `uv run --env-file`).
    """
    global _client
    if _client is None:
        _client = Langfuse()
    return _client
