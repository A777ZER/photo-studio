from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from back.app.core.config import settings


# Создаем подключение к базе данных
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
)


# Фабрика сессий SQLAlchemy
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)
