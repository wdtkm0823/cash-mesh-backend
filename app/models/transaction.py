from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"), nullable=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_type: TransactionType = Column(SQLEnum(TransactionType), nullable=False)  # type: ignore
    description = Column(String(255), nullable=True)
    transaction_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # リレーション
    user = relationship("User", backref="transactions")
    category = relationship("Category", backref="transactions")

    def __repr__(self):
        return f"<Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type}, user_id={self.user_id})>"
