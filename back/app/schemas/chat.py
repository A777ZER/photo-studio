
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Создание сообщения
class ChatMessageCreate(BaseModel):

    recipient_id: int = Field(gt=0)
    message: str = Field(
        min_length=1,
        max_length=5000,
    )


# Ответ с информацией о сообщении
class ChatMessageResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    sender_id: int
    recipient_id: int
    message: str
    created_at: datetime
