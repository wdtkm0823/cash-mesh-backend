from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

# エンジン作成
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # SQLログ出力（開発時）
    pool_pre_ping=True    # 接続確認
)

# セッションファクトリー
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラス
Base = declarative_base()


# 依存性注入用のDB取得関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
