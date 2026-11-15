
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
from back.app.models.service import Service
from back.app.models.user import User
from back.app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
)


router = APIRouter(
    prefix="/services",
    tags=["Услуги"],
)


# Получение списка активных услуг
@router.get(
    "/",
    response_model=list[ServiceResponse],
)
def get_services(
    db: Session = Depends(get_db),
):
    statement = (
        select(Service)
        .where(Service.is_active.is_(True))
        .order_by(Service.id)
    )

    return db.scalars(statement).all()


# Получение конкретной услуги
@router.get(
    "/{service_id}",
    response_model=ServiceResponse,
)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
):
    service = db.get(Service, service_id)

    if service is None or not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )

    return service


# Создание услуги администратором
@router.post(
    "/",
    response_model=ServiceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_service(
    service_data: ServiceCreate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    service = Service(**service_data.model_dump())

    try:
        db.add(service)
        db.commit()
        db.refresh(service)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Услуга с таким названием уже существует",
        )

    return service


# Редактирование услуги администратором
@router.patch(
    "/{service_id}",
    response_model=ServiceResponse,
)
def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    service = db.get(Service, service_id)

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )

    update_data = service_data.model_dump(
        exclude_unset=True,
    )

    for field, value in update_data.items():
        setattr(service, field, value)

    try:
        db.commit()
        db.refresh(service)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Услуга с таким названием уже существует",
        )

    return service


# Деактивация услуги администратором
@router.delete(
    "/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deactivate_service(
    service_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    service = db.get(Service, service_id)

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Услуга не найдена",
        )

    service.is_active = False

    db.commit()

    return None
