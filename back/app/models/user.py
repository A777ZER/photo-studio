
from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from back.app.db.base import Base


class User(Base):

    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "role IN ('client', 'photographer', 'admin')",
            name="valid_user_role",
        ),
    )

    # Идентификатор пользователя
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Электронная почта
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # Хеш пароля
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Имя
    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Фамилия
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Номер телефона
    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # Роль пользователя
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="client",
    )

    # Статус активности аккаунта
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Дата создания аккаунта
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
