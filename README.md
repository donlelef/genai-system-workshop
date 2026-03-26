# Chat With Your Data Workshop

Three hands-on projects that explore different approaches to building chat-with-your-data systems using LLMs: **Retrieval-Augmented Generation (RAG)**, an **agentic assistant**, and **Text-to-SQL**. Each project lives in its own directory with a self-contained `justfile` for running tasks.

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)
- [just](https://github.com/casey/just) (command runner)
- Docker (for Qdrant and PostgreSQL)

Install Python dependencies from the repository root:

```bash
uv sync
```

Each project requires a `.env` file — copy `.env.example` and fill in your keys.

## RAG — Retrieval-Augmented Generation

A movie recommendation assistant that answers questions by searching a local vector store of movie overviews. Supports two vector database backends: [LanceDB](https://lancedb.com/) (embedded) and [Qdrant](https://qdrant.tech/) (containerised).

### Running with LanceDB (no Docker needed)

```bash
cd rag
just populate-lancedb
just query-lancedb "What are some good sci-fi movies about time travel?"
```

### Running with Qdrant

```bash
cd rag
docker compose up -d
just populate-qdrant
just query-qdrant "What are some good sci-fi movies about time travel?"
```

## Agent — Crypto Portfolio Assistant

An agentic chatbot called **CryptoMax** that manages a cryptocurrency portfolio. It combines three capabilities via MCP (Model Context Protocol) tool servers:

1. **Price lookup** — real-time prices from the CoinGecko API
2. **Portfolio holdings** — a local MCP server that exposes the client's holdings
3. **Web search** — DuckDuckGo search for the latest crypto news

The agent runs as a web application powered by [Agno](https://github.com/agno-agi/agno) AgentOS.

### Running

```bash
cd agent
just run-all
```

The agent UI is available at <http://localhost:7777/docs>.

## Text-to-SQL — E-Commerce Data Analyst

A natural-language-to-SQL agent called **DataAnalyst** that queries an e-commerce PostgreSQL database. It discovers tables and schemas via an MCP server, writes SQL, executes it, and presents results to the user. Includes an evaluation harness that measures query accuracy against a ground-truth dataset.

### Running

```bash
cd text2sql
just run-all
```

The agent UI is available at <http://localhost:7777/docs>.

### Evaluation

```bash
just evaluate
```

To shut down the database:

```bash
just db-down
```

## License

MIT
