
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

import jwt

from back.app.core.config import settings
from back.app.db.session import SessionLocal
from back.app.models.chat import ChatMessage
from back.app.models.user import User


router = APIRouter()


class ConnectionManager:
    """Управление WebSocket-подключениями."""

    def __init__(self):
        self.active_connections: dict[
            tuple[int, int],
            list[WebSocket],
        ] = {}

    async def connect(
        self,
        websocket: WebSocket,
        conversation_id: tuple[int, int],
    ):
        await websocket.accept()

        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = []

        self.active_connections[conversation_id].append(websocket)

    def disconnect(
        self,
        websocket: WebSocket,
        conversation_id: tuple[int, int],
    ):
        connections = self.active_connections.get(conversation_id)

        if connections and websocket in connections:
            connections.remove(websocket)

            if not connections:
                del self.active_connections[conversation_id]

    async def broadcast(
        self,
        message: dict,
        conversation_id: tuple[int, int],
    ):
        connections = self.active_connections.get(
            conversation_id,
            [],
        )

        for connection in connections.copy():
            try:
                await connection.send_json(message)

            except Exception:
                self.disconnect(
                    connection,
                    conversation_id,
                )


manager = ConnectionManager()


# Получение пользователя по JWT из HttpOnly cookie
def get_user_from_token(
    websocket: WebSocket,
    db: Session,
) -> User | None:
    token = websocket.cookies.get(settings.cookie_name)

    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        user_id = int(payload.get("sub"))

    except (jwt.InvalidTokenError, ValueError, TypeError):
        return None

    user = db.get(User, user_id)

    if user is None or not user.is_active:
        return None

    return user


# WebSocket-подключение к переписке
@router.websocket("/ws/chat/{user_id}")
async def chat_websocket(
    websocket: WebSocket,
    user_id: int,
):
    db = SessionLocal()

    conversation_id = None
    connected = False

    try:
        # Проверяем авторизацию
        current_user = get_user_from_token(
            websocket,
            db,
        )

        if current_user is None:
            await websocket.close(code=1008)
            return

        # Чат доступен только клиентам и администраторам
        if current_user.role not in ("client", "admin"):
            await websocket.close(code=1008)
            return

        # Получаем второго участника переписки
        other_user = db.get(User, user_id)

        if other_user is None or not other_user.is_active:
            await websocket.close(code=1008)
            return

        # Проверяем допустимые роли участников
        valid_roles = (
            current_user.role == "client"
            and other_user.role == "admin"
        ) or (
            current_user.role == "admin"
            and other_user.role == "client"
        )

        if not valid_roles or current_user.id == other_user.id:
            await websocket.close(code=1008)
            return

        # Формируем общий идентификатор переписки
        conversation_id = tuple(
            sorted((current_user.id, other_user.id))
        )

        await manager.connect(
            websocket,
            conversation_id,
        )

        connected = True

        # Принимаем и обрабатываем сообщения
        while True:
            try:
                data = await websocket.receive_json()

            except ValueError:
                await websocket.send_json({
                    "error": "Некорректный формат JSON",
                })
                continue

            if not isinstance(data, dict):
                await websocket.send_json({
                    "error": "Неверный формат сообщения",
                })
                continue

            message_text = data.get("message")

            if not isinstance(message_text, str):
                await websocket.send_json({
                    "error": "Сообщение должно быть строкой",
                })
                continue

            message_text = message_text.strip()

            if not message_text or len(message_text) > 5000:
                await websocket.send_json({
                    "error": "Сообщение должно содержать от 1 до 5000 символов",
                })
                continue

            # Сохраняем сообщение в базе данных
            message = ChatMessage(
                sender_id=current_user.id,
                recipient_id=other_user.id,
                message=message_text,
            )

            try:
                db.add(message)
                db.commit()
                db.refresh(message)

            except SQLAlchemyError:
                db.rollback()

                await websocket.send_json({
                    "error": "Не удалось сохранить сообщение",
                })
                continue

            # Подготавливаем ответ для участников переписки
            response = {
                "id": message.id,
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "message": message.message,
                "created_at": message.created_at.isoformat(),
            }

            # Отправляем сообщение всем подключениям переписки
            await manager.broadcast(
                response,
                conversation_id,
            )

    except WebSocketDisconnect:
        pass

    finally:
        # Удаляем подключение независимо от причины завершения
        if connected and conversation_id is not None:
            manager.disconnect(
                websocket,
                conversation_id,
            )

        # Закрываем сессию базы данных
        db.close()
