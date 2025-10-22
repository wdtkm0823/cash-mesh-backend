from datetime import date
from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate


def get_transaction(db: Session, transaction_id: int):
    """トランザクションをIDで取得"""
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def get_transactions(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    transaction_type: str | None = None,
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    """ユーザーのトランザクション一覧を取得（フィルター対応）"""
    query = db.query(Transaction).filter(Transaction.user_id == user_id)

    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type) # type: ignore

    if category_id is not None:
        query = query.filter(Transaction.category_id == category_id)

    if start_date:
        query = query.filter(Transaction.transaction_date >= start_date)

    if end_date:
        query = query.filter(Transaction.transaction_date <= end_date)

    return query.order_by(Transaction.transaction_date.desc()).offset(skip).limit(limit).all()


def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    """トランザクションを作成"""
    db_transaction = Transaction(
        category_id=transaction.category_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        description=transaction.description,
        transaction_date=transaction.transaction_date,
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, db_transaction: Transaction, transaction: TransactionCreate):
    """トランザクションを更新"""
    for field_name, field_value in transaction.model_dump().items():
        setattr(db_transaction, field_name, field_value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, db_transaction: Transaction):
    """トランザクションを削除"""
    db.delete(db_transaction)
    db.commit()
