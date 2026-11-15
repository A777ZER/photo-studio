
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ServiceCreate(BaseModel):
    """Схема создания услуги."""

    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    duration_minutes: int = Field(gt=0, le=1440)
    price: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Название услуги не может быть пустым")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class ServiceUpdate(BaseModel):
    """Схема обновления услуги."""

    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    duration_minutes: int | None = Field(default=None, gt=0, le=1440)
    price: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Название услуги не может быть пустым")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("Необходимо указать данные для изменения")

        required_fields = (
            "name",
            "duration_minutes",
            "price",
            "is_active",
        )

        for field_name in required_fields:
            if (
                field_name in self.model_fields_set
                and getattr(self, field_name) is None
            ):
                raise ValueError(
                    f"Поле {field_name} не может быть пустым"
                )

        return self


class ServiceResponse(BaseModel):
    """Схема ответа с информацией об услуге."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    duration_minutes: int
    price: Decimal
    is_active: bool
    created_at: datetime
