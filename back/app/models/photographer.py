
from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from back.app.db.base import Base


class Photographer(Base):

    __tablename__ = "photographers"

    # Идентификатор профиля фотографа
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Связь с аккаунтом пользователя
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Специализация фотографа
    specialization: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Информация о фотографе
    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Связь с пользователем
    user: Mapped["User"] = relationship("User")
