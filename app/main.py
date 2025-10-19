from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import users, categories, transactions

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では制限する
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])


@app.get("/")
async def root():
    return {"message": "Cash Mesh API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
