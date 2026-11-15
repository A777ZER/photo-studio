from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from back.app.db.base import Base

#Отдельная позиция заказа на печать
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
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("print_orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    size: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )