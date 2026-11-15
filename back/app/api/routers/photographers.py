
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from back.app.dependencies.auth import require_role
from back.app.dependencies.database import get_db
from back.app.models.photographer import Photographer
from back.app.models.user import User
from back.app.schemas.photographer import (
    PhotographerCreate,
    PhotographerUpdate,
    PhotographerResponse,
)


router = APIRouter(
    prefix="/photographers",
    tags=["Фотографы"],
)


# Получение списка активных фотографов
@router.get(
    "/",
    response_model=list[PhotographerResponse],
)
def get_photographers(
    db: Session = Depends(get_db),
):
    statement = (
        select(Photographer)
        .join(User, Photographer.user_id == User.id)
        .where(User.is_active.is_(True))
        .order_by(Photographer.id)
    )

    return db.scalars(statement).all()


# Получение профиля фотографа
@router.get(
    "/{photographer_id}",
    response_model=PhotographerResponse,
)
def get_photographer(
    photographer_id: int,
    db: Session = Depends(get_db),
):
    statement = (
        select(Photographer)
        .join(User, Photographer.user_id == User.id)
        .where(
            Photographer.id == photographer_id,
            User.is_active.is_(True),
        )
    )

    photographer = db.scalars(statement).first()

    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотограф не найден",
        )

    return photographer


# Создание профиля фотографа администратором
@router.post(
    "/",
    response_model=PhotographerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_photographer(
    photographer_data: PhotographerCreate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    user = db.get(User, photographer_data.user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    if user.role != "photographer":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь должен иметь роль фотографа",
        )

    existing_profile = db.scalar(
        select(Photographer).where(
            Photographer.user_id == user.id
        )
    )

    if existing_profile is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Профиль фотографа уже существует",
        )

    photographer = Photographer(
        user_id=user.id,
        specialization=photographer_data.specialization,
        bio=photographer_data.bio,
    )

    try:
        db.add(photographer)
        db.commit()
        db.refresh(photographer)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Не удалось создать профиль фотографа",
        )

    return photographer


# Редактирование профиля фотографа администратором
@router.patch(
    "/{photographer_id}",
    response_model=PhotographerResponse,
)
def update_photographer(
    photographer_id: int,
    photographer_data: PhotographerUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    photographer = db.get(Photographer, photographer_id)

    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль фотографа не найден",
        )

    update_data = photographer_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(photographer, field, value)

    try:
        db.commit()
        db.refresh(photographer)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Не удалось обновить профиль фотографа",
        )

    return photographer
