
from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class PrintOrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Создание позиции заказа
class PrintOrderItemCreate(BaseModel):

    photo_id: int = Field(gt=0)
    size: str = Field(min_length=1, max_length=50)
    quantity: int = Field(default=1, gt=0)


# Изменение стоимости позиции администратором
class PrintOrderItemPriceUpdate(BaseModel):

    unit_price: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )


# Ответ с информацией о позиции заказа
class PrintOrderItemResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    photo_id: int
    size: str
    quantity: int
    unit_price: Decimal


# Создание заказа
class PrintOrderCreate(BaseModel):

    items: list[PrintOrderItemCreate] = Field(min_length=1)
    client_comment: str | None = Field(
        default=None,
        max_length=2000,
    )


# Изменение статуса заказа
class PrintOrderStatusUpdate(BaseModel):

    status: PrintOrderStatus
    admin_comment: str | None = Field(
        default=None,
        max_length=2000,
    )


# Ответ с информацией о заказе
class PrintOrderResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    status: PrintOrderStatus
    total_price: Decimal
    client_comment: str | None
    admin_comment: str | None
    created_at: datetime
    items: list[PrintOrderItemResponse]
