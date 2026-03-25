from langfuse import observe
from langfuse.openai import OpenAI

from rag.src.core.models import SearchResult
from rag.src.core.prompts import (
    HYDE_SYSTEM_PROMPT,
    RAG_SYSTEM_PROMPT,
    RAG_USER_TEMPLATE,
)

CHAT_MODEL = "gpt-4o-mini"

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


@observe(name="hyde-generate")
def generate_hypothetical_document(question: str) -> str:
    """Use HyDE to generate a hypothetical movie overview for the query."""
    response = _get_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": HYDE_SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or ""


@observe(name="rag-answer")
def generate_answer(question: str, results: list[SearchResult]) -> str:
    """Generate a final answer grounded in the retrieved movie context."""
    context_parts: list[str] = []
    for r in results:
        m = r.movie
        context_parts.append(f"- {m.title} ({m.release_date}, {m.genre}): {m.overview}")
    context = "\n".join(context_parts)

    response = _get_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": RAG_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": RAG_USER_TEMPLATE.format(context=context, question=question),
            },
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content or ""
