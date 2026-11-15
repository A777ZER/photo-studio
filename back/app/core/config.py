
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Корень проекта
PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Настройки приложения."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Основные настройки
    app_name: str = "Photo Studio"
    debug: bool = True

    # База данных
    database_url: str = (
        f"sqlite:///{PROJECT_ROOT / 'back/data/photostudio.db'}"
    )

    # Каталог фотографий
    storage_dir: Path = PROJECT_ROOT / "storage"

    # JWT
    jwt_secret_key: str = (
        "vXjEsDvTc7Qy7_RvEmGl9kc3Z9ahhoAPi5pcQUhqYnVUyOYIR"
        "uYzZeng8QruzFieFvITHv4BjMS2EOMKha_qf7g"
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15

    # Cookie
    cookie_secure: bool = False
    cookie_samesite: str = "lax"
    cookie_name: str = "access_token"

    # Frontend
    frontend_origin: str = "http://localhost:5173"


settings = Settings()
