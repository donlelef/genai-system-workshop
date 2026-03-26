import logging

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.mcp import MCPTools

from core.prompts import SYSTEM_INSTRUCTIONS
from infrastructure.logging_config import setup_logging
from infrastructure.tracing import configure_langfuse_tracing

logger = logging.getLogger(__name__)

MCP_URL = "http://127.0.0.1:8000/mcp"


def _create_agent() -> Agent:
    return Agent(
        id="text2sql-agent",
        name="DataAnalyst",
        model=OpenAIChat(id="gpt-5.4"),
        tools=[MCPTools(transport="streamable-http", url=MCP_URL)],
        instructions=SYSTEM_INSTRUCTIONS,
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True,
    )


def _create_agent_os() -> AgentOS:
    return AgentOS(
        description="Chat with your data — text-to-SQL agent",
        agents=[_create_agent()],
    )


setup_logging()
configure_langfuse_tracing()

_agent_os = _create_agent_os()
app = _agent_os.get_app()

if __name__ == "__main__":
    logger.info("Starting AgentOS on http://localhost:7777/docs")
    _agent_os.serve(app="scripts.run_agent:app")
