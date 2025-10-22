from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.crud import transaction as crud_transaction
from app.crud import category as crud_category
from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter()

# TODO: 認証実装後、user_idは認証トークンから取得する
# 現在は仮でuser_id=2を使用
TEMP_USER_ID = 2


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    # カテゴリーIDが指定されている場合、存在確認と所有者確認
    if transaction.category_id is not None:
        db_category = crud_category.get_category(db, category_id=transaction.category_id)
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        # TODO: 認証実装後、自分のカテゴリーかチェック
        if db_category.user_id != TEMP_USER_ID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to use this category"
            )

    return crud_transaction.create_transaction(db=db, transaction=transaction, user_id=TEMP_USER_ID)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # TODO: 認証実装後、自分のトランザクションかチェック
    if db_transaction.user_id != TEMP_USER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this transaction"
        )

    return db_transaction


@router.get("/", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = 0,
    limit: int = 100,
    transaction_type: str | None = Query(None, pattern="^(income|expense)$"),
    category_id: int | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    return crud_transaction.get_transactions(
        db,
        user_id=TEMP_USER_ID,
        skip=skip,
        limit=limit,
        transaction_type=transaction_type,
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # TODO: 認証実装後、自分のトランザクションかチェック
    if db_transaction.user_id != TEMP_USER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this transaction"
        )

    # カテゴリーIDが指定されている場合、存在確認と所有者確認
    if transaction.category_id is not None:
        db_category = crud_category.get_category(db, category_id=transaction.category_id)
        if not db_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        # TODO: 認証実装後、自分のカテゴリーかチェック
        if db_category.user_id != TEMP_USER_ID:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to use this category"
            )

    return crud_transaction.update_transaction(db=db, db_transaction=db_transaction, transaction=transaction)


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud_transaction.get_transaction(db, transaction_id=transaction_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    # TODO: 認証実装後、自分のトランザクションかチェック
    if db_transaction.user_id != TEMP_USER_ID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this transaction"
        )

    crud_transaction.delete_transaction(db=db, db_transaction=db_transaction)
    return {"message": "Transaction deleted successfully"}
