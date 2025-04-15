from pydantic import BaseModel, ConfigDict
from typing import Optional


class WalletCreate(BaseModel):
    address: str


class WalletResponse(BaseModel):
    id: Optional[int] = None
    address: str
    bandwidth: int
    energy: int
    trx_balance: float
    timestamp: Optional[float] = None

    model_config = ConfigDict(
        from_attributes=True
    )
