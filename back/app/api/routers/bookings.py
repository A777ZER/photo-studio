
from datetime import datetime, timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.orm import Session

from back.app.dependencies.auth import get_current_user, require_role
from back.app.dependencies.database import get_db
from back.app.models.availibility import PhotographerAvailability
from back.app.models.bookings import Booking
from back.app.models.photographer import Photographer
from back.app.models.service import Service
from back.app.models.user import User
from back.app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingStatusUpdate,
    BookingResponse,
)


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


# Продолжительность перерыва между фотосессиями
BOOKING_BUFFER = timedelta(minutes=15)


# Получение профиля активного фотографa
def get_active_photographer(
    photographer_id: int,
    db: Session,
) -> Photographer:
    statement = (
        select(Photographer)
        .join(User, Photographer.user_id == User.id)
        .where(
            Photographer.id == photographer_id,
            User.is_active.is_(True),
            User.role == "photographer",
        )
    )

    photographer = db.scalars(statement).first()

    if photographer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотограф не найден или неактивен",
        )

    return photographer


# Проверка попадания бронирования в рабочее расписание
def check_photographer_availability(
    db: Session,
    photographer_id: int,
    start_at: datetime,
    end_at: datetime,
):
    statement = select(PhotographerAvailability).where(
        PhotographerAvailability.photographer_id == photographer_id,
        PhotographerAvailability.start_at <= start_at,
        PhotographerAvailability.end_at >= end_at,
    )

    availability = db.scalars(statement).first()

    if availability is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Выбранное время не входит в рабочее расписание фотографа",
        )


# Проверка пересечения с подтверждёнными бронированиями
def check_booking_conflicts(
    db: Session,
    photographer_id: int,
    start_at: datetime,
    end_at: datetime,
    exclude_booking_id: int | None = None,
):
    statement = select(Booking).where(
        Booking.photographer_id == photographer_id,
        Booking.status == "confirmed",
        Booking.start_at < end_at + BOOKING_BUFFER,
        Booking.end_at > start_at - BOOKING_BUFFER,
    )

    if exclude_booking_id is not None:
        statement = statement.where(
            Booking.id != exclude_booking_id
        )

    conflicting_booking = db.scalars(statement).first()

    if conflicting_booking is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Выбранное время занято или не соблюдается перерыв между фотосессиями",
        )


# Общая проверка доступности времени
def validate_booking_time(
    db: Session,
    photographer_id: int,
    start_at: datetime,
    end_at: datetime,
    exclude_booking_id: int | None = None,
):
    check_photographer_availability(
        db=db,
        photographer_id=photographer_id,
        start_at=start_at,
        end_at=end_at,
    )

    check_booking_conflicts(
        db=db,
        photographer_id=photographer_id,
        start_at=start_at,
        end_at=end_at,
        exclude_booking_id=exclude_booking_id,
    )


# Создание нового бронирования клиентом
@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(require_role("client")),
    db: Session = Depends(get_db),
):
    photographer = get_active_photographer(
        booking_data.photographer_id,
        db,
    )

    service = db.get(Service, booking_data.service_id)

    if service is None or not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена или неактивна",
        )

    end_at = booking_data.start_at + timedelta(
        minutes=service.duration_minutes
    )

    # Проверяем рабочее расписание.
    # Ожидающие бронирования не блокируют время.
    check_photographer_availability(
        db=db,
        photographer_id=photographer.id,
        start_at=booking_data.start_at,
        end_at=end_at,
    )

    booking = Booking(
        client_id=current_user.id,
        photographer_id=photographer.id,
        service_id=service.id,
        start_at=booking_data.start_at,
        end_at=end_at,
        status="waiting",
        price=service.price,
        client_comment=booking_data.client_comment,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


# Получение списка бронирований с учётом роли пользователя
@router.get(
    "/",
    response_model=list[BookingResponse],
)
def get_bookings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    statement = select(Booking)

    if current_user.role == "client":
        statement = statement.where(
            Booking.client_id == current_user.id
        )

    elif current_user.role == "photographer":
        photographer = db.scalars(
            select(Photographer).where(
                Photographer.user_id == current_user.id
            )
        ).first()

        if photographer is None:
            return []

        statement = statement.where(
            Booking.photographer_id == photographer.id
        )

    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )

    statement = statement.order_by(
        Booking.start_at.desc()
    )

    return db.scalars(statement).all()


# Изменение клиентом собственного бронирования
@router.patch(
    "/{booking_id}",
    response_model=BookingResponse,
)
def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: User = Depends(require_role("client")),
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None or booking.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено",
        )

    if booking.status != "waiting":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Изменять можно только ожидающие бронирования",
        )

    if booking_data.start_at is not None:
        photographer = get_active_photographer(
            booking.photographer_id,
            db,
        )

        service = db.get(Service, booking.service_id)

        if service is None or not service.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Услуга не найдена или неактивна",
            )

        new_start = booking_data.start_at
        new_end = new_start + timedelta(
            minutes=service.duration_minutes
        )

        check_photographer_availability(
            db=db,
            photographer_id=photographer.id,
            start_at=new_start,
            end_at=new_end,
        )

        booking.start_at = new_start
        booking.end_at = new_end

    if "client_comment" in booking_data.model_fields_set:
        booking.client_comment = booking_data.client_comment

    db.commit()
    db.refresh(booking)

    return booking


# Изменение статуса бронирования администратором
@router.patch(
    "/{booking_id}/status",
    response_model=BookingResponse,
)
def update_booking_status(
    booking_id: int,
    status_data: BookingStatusUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    booking = db.get(Booking, booking_id)

    if booking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Бронирование не найдено",
        )

    # При подтверждении проверяем доступность времени
    if status_data.status == "confirmed":
        get_active_photographer(
            booking.photographer_id,
            db,
        )

        validate_booking_time(
            db=db,
            photographer_id=booking.photographer_id,
            start_at=booking.start_at,
            end_at=booking.end_at,
            exclude_booking_id=booking.id,
        )

    booking.status = status_data.status

    if "admin_comment" in status_data.model_fields_set:
        booking.admin_comment = status_data.admin_comment

    db.commit()
    db.refresh(booking)

    return booking
