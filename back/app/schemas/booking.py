
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


BookingStatus = Literal[
    "waiting",
    "confirmed",
    "completed",
    "canceled",
    "no_show",
]


def validate_timezone(value: datetime) -> datetime:
    """Проверка наличия часового пояса у даты и времени."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(
            "Дата и время должны содержать часовой пояс"
        )

    return value


class BookingCreate(BaseModel):
    """Схема создания бронирования."""

    photographer_id: int = Field(gt=0)
    service_id: int = Field(gt=0)
    start_at: datetime
    client_comment: str | None = Field(
        default=None,
        max_length=2000,
    )

    @field_validator("start_at")
    @classmethod
    def validate_start_at(cls, value: datetime) -> datetime:
        return validate_timezone(value)

    @field_validator("client_comment")
    @classmethod
    def validate_client_comment(
        cls,
        value: str | None,
    ) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class BookingUpdate(BaseModel):
    """Схема изменения бронирования."""

    start_at: datetime | None = None
    client_comment: str | None = Field(
        default=None,
        max_length=2000,
    )

    @field_validator("start_at")
    @classmethod
    def validate_start_at(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is not None:
            return validate_timezone(value)

        return value

    @field_validator("client_comment")
    @classmethod
    def validate_client_comment(
        cls,
        value: str | None,
    ) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError(
                "Необходимо указать данные для изменения"
            )

        if (
            "start_at" in self.model_fields_set
            and self.start_at is None
        ):
            raise ValueError(
                "Дата и время начала записи не могут быть пустыми"
            )

        return self


class BookingStatusUpdate(BaseModel):
    """Схема изменения статуса бронирования."""

    status: BookingStatus
    admin_comment: str | None = Field(
        default=None,
        max_length=2000,
    )

    @field_validator("admin_comment")
    @classmethod
    def validate_admin_comment(
        cls,
        value: str | None,
    ) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class BookingResponse(BaseModel):
    """Схема ответа с информацией о бронировании."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    photographer_id: int
    service_id: int
    start_at: datetime
    end_at: datetime
    status: BookingStatus
    price: Decimal
    client_comment: str | None
    admin_comment: str | None
