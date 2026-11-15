
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
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from back.app.db.base import Base


# Заказ клиента на печать фотографий
class PrintOrder(Base):

    __tablename__ = "print_orders"

    __table_args__ = (
        CheckConstraint(
            "total_price >= 0",
            name="nonnegative_total_price",
        ),
        CheckConstraint(
            "status IN ('pending', 'processing', 'completed', 'cancelled')",
            name="valid_status",
        ),
    )

    # Идентификатор заказа
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Клиент, оформивший заказ
    client_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Статус заказа
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
        index=True,
    )

    # Общая стоимость заказа
    total_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
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

    # Дата создания заказа
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    # Позиции заказа
    items: Mapped[list["PrintOrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


# Отдельная позиция заказа на печать
class PrintOrderItem(Base):

    __tablename__ = "print_order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="positive_quantity",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="nonnegative_unit_price",
        ),
        CheckConstraint(
            "length(trim(size)) > 0",
            name="nonempty_print_size",
        ),
    )

    # Идентификатор позиции
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # Заказ, к которому относится позиция
    order_id: Mapped[int] = mapped_column(
        ForeignKey("print_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Фотография для печати
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Размер печати
    size: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Количество экземпляров
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    # Стоимость одного экземпляра
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    # Связь с заказом
    order: Mapped["PrintOrder"] = relationship(
        back_populates="items",
    )
