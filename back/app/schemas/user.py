
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


class UserRegister(BaseModel):
    """Схема регистрации пользователя."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Поле не может быть пустым")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class UserLogin(BaseModel):
    """Схема авторизации пользователя."""

    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str | None
    role: str
    is_active: bool
    created_at: datetime


class UserUpdate(BaseModel):
    """Схема обновления личных данных пользователя."""

    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=30)

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                raise ValueError("Имя и фамилия не могут быть пустыми")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value

    @model_validator(mode="after")
    def validate_update_data(self):
        if not self.model_fields_set:
            raise ValueError(
                "Необходимо указать хотя бы одно поле для обновления"
            )

        if "first_name" in self.model_fields_set and self.first_name is None:
            raise ValueError("Имя не может быть пустым")

        if "last_name" in self.model_fields_set and self.last_name is None:
            raise ValueError("Фамилия не может быть пустой")

        return self
