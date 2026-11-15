
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from back.app.db.base import Base


# Метаданные фотографии, хранящейся на диске
class Photo(Base):

    __tablename__ = "photos"

    # Идентификатор фотографии
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Владелец фотографии
    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Пользователь, загрузивший фотографию
    uploaded_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Исходное имя файла
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Путь к файлу на сервере
    storage_path: Mapped[str] = mapped_column(
        String(500),
        unique=True,
        nullable=False,
    )

    # MIME-тип файла
    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Дата загрузки фотографии
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
