
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from back.app.dependencies.auth import get_current_user
from back.app.dependencies.database import get_db
from back.app.models.availibility import PhotographerAvailability
from back.app.models.photographer import Photographer
from back.app.models.user import User
from back.app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityUpdate,
    AvailabilityResponse,
)


router = APIRouter(
    prefix="/availability",
    tags=["Расписание"],
)


# Проверка прав доступа к расписанию фотографа
def check_photographer_access(
    photographer: Photographer | None,
    current_user: User,
):
    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль фотографа не найден",
        )

    if (
        current_user.role != "admin"
        and (
            current_user.role != "photographer"
            or photographer.user_id != current_user.id
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )


# Проверка пересечения рабочих интервалов
def check_availability_overlap(
    db: Session,
    photographer_id: int,
    start_at,
    end_at,
    exclude_id: int | None = None,
):
    statement = select(PhotographerAvailability).where(
        PhotographerAvailability.photographer_id == photographer_id,
        PhotographerAvailability.start_at < end_at,
        PhotographerAvailability.end_at > start_at,
    )

    if exclude_id is not None:
        statement = statement.where(
            PhotographerAvailability.id != exclude_id
        )

    overlapping = db.scalars(statement).first()

    if overlapping is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Рабочий интервал пересекается с существующим",
        )


# Получение рабочих интервалов фотографа
@router.get(
    "/photographers/{photographer_id}",
    response_model=list[AvailabilityResponse],
)
def get_photographer_availability(
    photographer_id: int,
    db: Session = Depends(get_db),
):
    photographer = db.get(Photographer, photographer_id)

    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотограф не найден",
        )

    statement = (
        select(PhotographerAvailability)
        .where(
            PhotographerAvailability.photographer_id == photographer_id
        )
        .order_by(PhotographerAvailability.start_at)
    )

    return db.scalars(statement).all()


# Создание рабочего интервала
@router.post(
    "/",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_availability(
    availability_data: AvailabilityCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role == "photographer":
        photographer = db.scalar(
            select(Photographer).where(
                Photographer.user_id == current_user.id
            )
        )

    elif current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Для создания расписания администратора необходимо указать фотографа",
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )

    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Профиль фотографа не найден",
        )

    check_availability_overlap(
        db=db,
        photographer_id=photographer.id,
        start_at=availability_data.start_at,
        end_at=availability_data.end_at,
    )

    availability = PhotographerAvailability(
        photographer_id=photographer.id,
        start_at=availability_data.start_at,
        end_at=availability_data.end_at,
        note=availability_data.note,
    )

    try:
        db.add(availability)
        db.commit()
        db.refresh(availability)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Не удалось создать рабочий интервал",
        )

    return availability


# Изменение рабочего интервала
@router.patch(
    "/{availability_id}",
    response_model=AvailabilityResponse,
)
def update_availability(
    availability_id: int,
    availability_data: AvailabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    availability = db.get(
        PhotographerAvailability,
        availability_id,
    )

    if availability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рабочий интервал не найден",
        )

    photographer = db.get(
        Photographer,
        availability.photographer_id,
    )

    check_photographer_access(
        photographer,
        current_user,
    )

    new_start = (
        availability_data.start_at
        if availability_data.start_at is not None
        else availability.start_at
    )

    new_end = (
        availability_data.end_at
        if availability_data.end_at is not None
        else availability.end_at
    )

    if new_end <= new_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время окончания должно быть позже времени начала",
        )

    check_availability_overlap(
        db=db,
        photographer_id=availability.photographer_id,
        start_at=new_start,
        end_at=new_end,
        exclude_id=availability.id,
    )

    availability.start_at = new_start
    availability.end_at = new_end

    if "note" in availability_data.model_fields_set:
        availability.note = availability_data.note

    try:
        db.commit()
        db.refresh(availability)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Не удалось обновить рабочий интервал",
        )

    return availability


# Удаление рабочего интервала
@router.delete(
    "/{availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_availability(
    availability_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    availability = db.get(
        PhotographerAvailability,
        availability_id,
    )

    if availability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Рабочий интервал не найден",
        )

    photographer = db.get(
        Photographer,
        availability.photographer_id,
    )

    check_photographer_access(
        photographer,
        current_user,
    )

    db.delete(availability)
    db.commit()

    return None
