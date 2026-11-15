
from fastapi import APIRouter

from back.app.api.routers import (
    auth,
    availibility,
    bookings,
    chat,
    photographers,
    photos,
    print_orders,
    services,
)

from back.app.websocket.chat import router as websocket_chat_router


# Главный маршрутизатор API
router = APIRouter(prefix="/api")


# HTTP API
router.include_router(auth.router)
router.include_router(availibility.router)
router.include_router(bookings.router)
router.include_router(chat.router)
router.include_router(photographers.router)
router.include_router(photos.router)
router.include_router(print_orders.router)
router.include_router(services.router)


# WebSocket
router.include_router(websocket_chat_router)

