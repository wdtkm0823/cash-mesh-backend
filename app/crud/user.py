from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id: int):
    """ユーザーをIDで取得"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """ユーザーをメールアドレスで取得"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """ユーザーをユーザー名で取得"""
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """ユーザー一覧を取得"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    """ユーザーを作成"""
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: User, user: UserCreate):
    """ユーザーを更新"""
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, db_user: User):
    """ユーザーを削除"""
    db.delete(db_user)
    db.commit()
