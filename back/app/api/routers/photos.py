
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from back.app.core.config import settings
from back.app.dependencies.auth import get_current_user
from back.app.dependencies.database import get_db
from back.app.models.photo import Photo
from back.app.models.user import User
from back.app.schemas.photo import PhotoResponse


router = APIRouter(
    prefix="/photos",
    tags=["Фотографии"],
)


# Разрешённые форматы фотографий
ALLOWED_MIME_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}

# Максимальный размер файла — 10 МБ
MAX_FILE_SIZE = 10 * 1024 * 1024

# Размер одного фрагмента при чтении файла
CHUNK_SIZE = 1024 * 1024


# Загрузка фотографии клиентом
@router.post(
    "/",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_photo(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role != "client":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Загружать фотографии могут только клиенты",
        )

    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Недопустимый формат фотографии",
        )

    expected_mime_type = ALLOWED_MIME_TYPES[extension]

    if file.content_type != expected_mime_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тип файла не соответствует его расширению",
        )

    storage_dir = Path(settings.storage_dir) / "photos"
    storage_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}{extension}"
    file_path = storage_dir / filename

    file_size = 0

    try:
        with file_path.open("wb") as buffer:
            while chunk := file.file.read(CHUNK_SIZE):
                file_size += len(chunk)

                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail="Размер фотографии не должен превышать 10 МБ",
                    )

                buffer.write(chunk)

        if file_size == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Загруженный файл пуст",
            )

        photo = Photo(
            client_id=current_user.id,
            uploaded_by_id=current_user.id,
            original_filename=file.filename,
            storage_path=str(file_path),
            mime_type=expected_mime_type,
        )

        db.add(photo)
        db.commit()
        db.refresh(photo)

    except Exception:
        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise

    return photo


# Получение списка фотографий
@router.get(
    "/",
    response_model=list[PhotoResponse],
)
def get_photos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role not in ("client", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра фотографий",
        )

    statement = select(Photo)

    if current_user.role == "client":
        statement = statement.where(
            Photo.client_id == current_user.id
        )

    statement = statement.order_by(
        Photo.created_at.desc()
    )

    return db.scalars(statement).all()


# Удаление фотографии
@router.delete(
    "/{photo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_photo(
    photo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    photo = db.get(Photo, photo_id)

    if photo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотография не найдена",
        )

    if (
        current_user.role != "admin"
        and (
            current_user.role != "client"
            or photo.client_id != current_user.id
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для удаления фотографии",
        )

    file_path = Path(photo.storage_path)

    # Удаляем запись из базы данных
    db.delete(photo)
    db.commit()

    # Удаляем физический файл
    try:
        if file_path.exists():
            file_path.unlink()

    except OSError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Запись удалена, но не удалось удалить файл с диска",
        )

    return None
