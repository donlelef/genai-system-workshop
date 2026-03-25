from langfuse import observe
from langfuse.openai import OpenAI

from rag.src.core.models import SearchResult
from rag.src.core.prompts import (
    HYDE_SYSTEM_PROMPT,
    RAG_SYSTEM_PROMPT,
    RAG_USER_TEMPLATE,
)

CHAT_MODEL = "gpt-5.4"


@observe(name="hyde-generate")
def generate_hypothetical_document(question: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=HYDE_SYSTEM_PROMPT,
        input=question,
        temperature=0.7,
        store=False,
    )
    return response.output_text or ""


@observe(name="rag-answer")
def generate_answer(question: str, results: list[SearchResult]) -> str:
    client = OpenAI()
    context_parts: list[str] = []
    for r in results:
        m = r.movie
        context_parts.append(f"- {m.title} ({m.release_date}, {m.genre}): {m.overview}")
    context = "\n".join(context_parts)

    response = client.responses.create(
        model=CHAT_MODEL,
        instructions=RAG_SYSTEM_PROMPT,
        input=RAG_USER_TEMPLATE.format(context=context, question=question),
        temperature=0.3,
        store=False,
    )
    return response.output_text or ""
