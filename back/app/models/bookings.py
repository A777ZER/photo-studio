
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from back.app.db.base import Base


class Booking(Base):
    """Модель бронирования фотосессии."""

    __tablename__ = "bookings"

    # Проверка ограничений
    __table_args__ = (
        CheckConstraint(
            "end_at > start_at",
            name="valid_time_range",
        ),
        CheckConstraint(
            "price >= 0",
            name="nonnegative_price",
        ),
        CheckConstraint(
            "status IN ('waiting', 'confirmed', 'completed', "
            "'canceled', 'no_show')",
            name="valid_status",
        ),
    )

    # Идентификатор бронирования
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Клиент, создавший бронирование
    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Фотограф, проводящий фотосессию
    photographer_id: Mapped[int] = mapped_column(
        ForeignKey("photographers.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Выбранная услуга
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Время начала фотосессии
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # Время окончания фотосессии
    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Статус бронирования
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="waiting",
        index=True,
    )

    # Стоимость бронирования
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # Комментарий клиента
    client_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Комментарий администратора
    admin_comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
