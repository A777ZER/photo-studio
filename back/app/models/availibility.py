
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from back.app.db.base import Base


# Таблица интервала доступности фотографа
class PhotographerAvailability(Base):

    __tablename__ = "photographer_availability"

    __table_args__ = (
        CheckConstraint(
            "end_at > start_at",
            name="valid_time_range",
        ),
    )

    # Идентификатор интервала
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Фотограф, которому принадлежит интервал
    photographer_id: Mapped[int] = mapped_column(
        ForeignKey("photographers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Начало рабочего интервала
    start_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # Окончание рабочего интервала
    end_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Дополнительная информация
    note: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Связь с фотографом
    photographer: Mapped["Photographer"] = relationship(
        "Photographer"
    )
