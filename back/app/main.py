
from fastapi import FastAPI

from back.app.core.config import settings
from back.app.api.routers.router import router


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


# Подключение всех маршрутов API
app.include_router(router)


@app.get("/")
def read_root():
    return {
        "message": "Photo Studio API is running",
        "app_name": settings.app_name,
    }


@app.get("/health")
def health_check():
    return {
        "message": "Status OK",
    }
