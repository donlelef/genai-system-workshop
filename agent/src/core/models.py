from typing import Literal

from pydantic import BaseModel, Field

CryptoName = Literal["bitcoin", "ethereum", "solana", "cardano", "polkadot"]


class PortfolioHolding(BaseModel):
    crypto: CryptoName = Field(description="Cryptocurrency identifier")
    amount: float = Field(description="Number of coins held")


class PortfolioSummary(BaseModel):
    holdings: dict[CryptoName, float] = Field(
        description="Map of cryptocurrency name to amount held"
    )
