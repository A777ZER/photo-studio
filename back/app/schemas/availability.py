
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


def validate_timezone(value: datetime) -> datetime:
    """Проверка наличия корректного часового пояса."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(
            "Дата и время должны содержать часовой пояс"
        )

    return value


class AvailabilityCreate(BaseModel):
    """Схема создания рабочего интервала фотографа."""

    start_at: datetime
    end_at: datetime
    note: str | None = Field(default=None, max_length=500)

    @field_validator("start_at", "end_at")
    @classmethod
    def validate_datetime(cls, value: datetime) -> datetime:
        return validate_timezone(value)

    @field_validator("note")
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @model_validator(mode="after")
    def validate_interval(self):
        if self.end_at <= self.start_at:
            raise ValueError(
                "Время окончания должно быть позже времени начала"
            )

        return self


class AvailabilityUpdate(BaseModel):
    """Схема изменения рабочего интервала фотографа."""

    start_at: datetime | None = None
    end_at: datetime | None = None
    note: str | None = Field(default=None, max_length=500)

    @field_validator("start_at", "end_at")
    @classmethod
    def validate_datetime(
        cls,
        value: datetime | None,
    ) -> datetime | None:
        if value is not None:
            return validate_timezone(value)

        return value

    @field_validator("note")
    @classmethod
    def validate_note(cls, value: str | None) -> str | None:
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

        for field_name in ("start_at", "end_at"):
            if (
                field_name in self.model_fields_set
                and getattr(self, field_name) is None
            ):
                raise ValueError(
                    f"Поле {field_name} не может быть пустым"
                )

        if (
            self.start_at is not None
            and self.end_at is not None
            and self.end_at <= self.start_at
        ):
            raise ValueError(
                "Время окончания должно быть позже времени начала"
            )

        return self


class AvailabilityResponse(BaseModel):
    """Схема ответа с информацией о рабочем интервале."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    photographer_id: int
    start_at: datetime
    end_at: datetime
    note: str | None
