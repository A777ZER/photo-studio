
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class PhotographerCreate(BaseModel):
    """Схема создания профиля фотографа."""

    user_id: int = Field(gt=0)
    specialization: str | None = Field(default=None, max_length=150)
    bio: str | None = Field(default=None, max_length=5000)

    @field_validator("specialization", "bio")
    @classmethod
    def validate_text(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value


class PhotographerUpdate(BaseModel):
    """Схема обновления профиля фотографа."""

    specialization: str | None = Field(default=None, max_length=150)
    bio: str | None = Field(default=None, max_length=5000)

    @field_validator("specialization", "bio")
    @classmethod
    def validate_text(cls, value: str | None) -> str | None:
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

        return self


class PhotographerResponse(BaseModel):
    """Схема ответа с данными фотографа."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    specialization: str | None
    bio: str | None
