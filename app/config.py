from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str | None = None

    # App
    APP_NAME: str = "Cash Mesh API"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # 余分な環境変数を無視
    )


settings = Settings()
