from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_category(db: Session, category_id: int):
    """カテゴリーをIDで取得"""
    return db.query(Category).filter(Category.id == category_id).first()


def get_categories(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """ユーザーのカテゴリー一覧を取得"""
    return db.query(Category).filter(Category.user_id == user_id).offset(skip).limit(limit).all()


def create_category(db: Session, category: CategoryCreate, user_id: int):
    """カテゴリーを作成"""
    db_category = Category(
        name=category.name,
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, db_category: Category, category: CategoryCreate):
    """カテゴリーを更新"""
    for field_name, field_value in category.model_dump().items():
        setattr(db_category, field_name, field_value)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, db_category: Category):
    """カテゴリーを削除"""
    db.delete(db_category)
    db.commit()
