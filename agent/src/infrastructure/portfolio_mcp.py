import logging
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

from infrastructure.logging_config import setup_logging
from core.models import CryptoName, PortfolioHolding, PortfolioSummary

logger = logging.getLogger(__name__)

mcp = FastMCP(name="PortfolioServer")


def _load_portfolio() -> dict[CryptoName, float]:
    return {
        "bitcoin": 1.5,
        "ethereum": 10.0,
        "solana": 50.0,
        "cardano": 5000.0,
        "polkadot": 200.0,
    }


@mcp.tool()
def get_portfolio(
    crypto: Annotated[
        CryptoName,
        Field(description="Cryptocurrency name, e.g. 'bitcoin', 'ethereum'"),
    ],
) -> PortfolioHolding:
    """Look up how many coins the client holds for a given cryptocurrency."""
    portfolio = _load_portfolio()
    logger.info("Portfolio lookup: %s -> %s", crypto, portfolio[crypto])
    return PortfolioHolding(crypto=crypto, amount=portfolio[crypto])


@mcp.tool()
def list_portfolio() -> PortfolioSummary:
    """List every cryptocurrency in the portfolio with its held amount."""
    logger.info("Full portfolio requested")
    return PortfolioSummary(holdings=_load_portfolio())


if __name__ == "__main__":
    setup_logging()
    logger.info("Starting Portfolio MCP server on 127.0.0.1:8000")
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
