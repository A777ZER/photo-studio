
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from back.app.db.base import Base


class Service(Base):

    __tablename__ = "services"

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="positive_service_duration",
        ),
        CheckConstraint(
            "price >= 0",
            name="nonnegative_service_price",
        ),
    )

    # Идентификатор услуги
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Название услуги
    name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    # Описание услуги
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Продолжительность услуги в минутах
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Стоимость услуги
    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # Статус активности услуги
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    # Дата создания услуги
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
