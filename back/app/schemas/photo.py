
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PhotoResponse(BaseModel):
    """Схема ответа с информацией о фотографии."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    uploaded_by_id: int
    original_filename: str
    mime_type: str
    created_at: datetime
