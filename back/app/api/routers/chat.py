
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from back.app.dependencies.auth import get_current_user
from back.app.dependencies.database import get_db
from back.app.models.chat import ChatMessage
from back.app.models.user import User
from back.app.schemas.chat import (
    ChatMessageCreate,
    ChatMessageResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Чат"],
)


# Проверка возможности общения двух пользователей
def validate_chat_participants(
    current_user: User,
    other_user: User,
):
    if current_user.role not in ("client", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Пользователю запрещено использовать чат",
        )

    if other_user is None or not other_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден или неактивен",
        )

    valid_roles = (
        current_user.role == "client"
        and other_user.role == "admin"
    ) or (
        current_user.role == "admin"
        and other_user.role == "client"
    )

    if not valid_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Переписка разрешена только между клиентами и администраторами",
        )


# Отправка сообщения
@router.post(
    "/messages",
    response_model=ChatMessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def send_message(
    message_data: ChatMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recipient = db.get(User, message_data.recipient_id)

    validate_chat_participants(
        current_user,
        recipient,
    )

    message_text = message_data.message.strip()

    if not message_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Сообщение не может быть пустым",
        )

    message = ChatMessage(
        sender_id=current_user.id,
        recipient_id=recipient.id,
        message=message_text,
    )

    try:
        db.add(message)
        db.commit()
        db.refresh(message)

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось отправить сообщение",
        )

    return message


# Получение истории переписки
@router.get(
    "/conversation/{user_id}",
    response_model=list[ChatMessageResponse],
)
def get_conversation(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    other_user = db.get(User, user_id)

    validate_chat_participants(
        current_user,
        other_user,
    )

    statement = (
        select(ChatMessage)
        .where(
            or_(
                (
                    (ChatMessage.sender_id == current_user.id)
                    & (ChatMessage.recipient_id == other_user.id)
                ),
                (
                    (ChatMessage.sender_id == other_user.id)
                    & (ChatMessage.recipient_id == current_user.id)
                ),
            )
        )
        .order_by(
            ChatMessage.created_at.asc(),
            ChatMessage.id.asc(),
        )
    )

    return db.scalars(statement).all()
