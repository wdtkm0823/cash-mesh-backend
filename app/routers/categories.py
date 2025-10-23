from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import category as crud_category
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    # TODO: 認証実装後、管理者権限チェックを追加
    return crud_category.create_category(db=db, category=category)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return db_category


@router.get("/", response_model=List[CategoryResponse])
def get_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_category.get_categories(db, skip=skip, limit=limit)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    # TODO: 認証実装後、管理者権限チェックを追加
    db_category = crud_category.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    return crud_category.update_category(db=db, db_category=db_category, category=category)


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    # TODO: 認証実装後、管理者権限チェックを追加
    db_category = crud_category.get_category(db, category_id=category_id)
    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    crud_category.delete_category(db=db, db_category=db_category)
    return {"message": "Category deleted successfully"}
