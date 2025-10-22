from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class TransactionBase(BaseModel):
    category_id: int | None = None
    amount: float = Field(gt=0, description="Amount must be greater than 0")
    transaction_type: Literal["income", "expense"]
    description: str | None = None
    transaction_date: date


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
