
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from back.app.dependencies.auth import get_current_user, require_role
from back.app.dependencies.database import get_db
from back.app.models.photo import Photo
from back.app.models.print_order import PrintOrder, PrintOrderItem
from back.app.models.user import User
from back.app.schemas.print_order import (
    PrintOrderCreate,
    PrintOrderItemPriceUpdate,
    PrintOrderResponse,
    PrintOrderStatusUpdate,
)


router = APIRouter(
    prefix="/print-orders",
    tags=["Заказы на печать"],
)


# Получение заказа вместе с его позициями
def get_order_with_items(
    order_id: int,
    db: Session,
) -> PrintOrder:
    statement = (
        select(PrintOrder)
        .options(selectinload(PrintOrder.items))
        .where(PrintOrder.id == order_id)
    )

    order = db.scalars(statement).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ на печать не найден",
        )

    return order


# Создание заказа на печать клиентом
@router.post(
    "/",
    response_model=PrintOrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_print_order(
    order_data: PrintOrderCreate,
    current_user: User = Depends(require_role("client")),
    db: Session = Depends(get_db),
):
    # Проверяем принадлежность всех фотографий клиенту
    for item_data in order_data.items:
        photo = db.get(Photo, item_data.photo_id)

        if photo is None or photo.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Фотография не найдена",
            )

    # Создаём заказ с нулевой стоимостью
    order = PrintOrder(
        client_id=current_user.id,
        status="pending",
        total_price=Decimal("0.00"),
        client_comment=order_data.client_comment,
    )

    try:
        db.add(order)
        db.flush()

        # Добавляем позиции без установленной стоимости
        for item_data in order_data.items:
            item = PrintOrderItem(
                order_id=order.id,
                photo_id=item_data.photo_id,
                size=item_data.size,
                quantity=item_data.quantity,
                unit_price=Decimal("0.00"),
            )

            db.add(item)

        db.commit()

    except (IntegrityError, SQLAlchemyError):
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось создать заказ на печать",
        )

    return get_order_with_items(order.id, db)


# Получение списка заказов
@router.get(
    "/",
    response_model=list[PrintOrderResponse],
)
def get_print_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    statement = select(PrintOrder).options(
        selectinload(PrintOrder.items)
    )

    if current_user.role == "client":
        statement = statement.where(
            PrintOrder.client_id == current_user.id
        )

    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра заказов",
        )

    statement = statement.order_by(
        PrintOrder.created_at.desc()
    )

    return db.scalars(statement).all()


# Получение конкретного заказа
@router.get(
    "/{order_id}",
    response_model=PrintOrderResponse,
)
def get_print_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = get_order_with_items(order_id, db)

    if current_user.role == "client":
        if order.client_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Недостаточно прав для просмотра этого заказа",
            )

    elif current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для просмотра заказов",
        )

    return order


# Изменение стоимости позиции администратором
@router.patch(
    "/items/{item_id}/price",
    response_model=PrintOrderResponse,
)
def update_print_order_item_price(
    item_id: int,
    price_data: PrintOrderItemPriceUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    item = db.get(PrintOrderItem, item_id)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Позиция заказа не найдена",
        )

    order = db.get(PrintOrder, item.order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ на печать не найден",
        )

    if order.status in ("completed", "cancelled"):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Нельзя изменять стоимость завершённого или отменённого заказа",
        )

    try:
        item.unit_price = price_data.unit_price

        # Пересчитываем общую стоимость всех позиций
        total_price = sum(
            (
                order_item.unit_price * order_item.quantity
                for order_item in order.items
            ),
            Decimal("0.00"),
        )

        order.total_price = total_price

        db.commit()

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось изменить стоимость заказа",
        )

    return get_order_with_items(order.id, db)


# Изменение статуса заказа администратором
@router.patch(
    "/{order_id}/status",
    response_model=PrintOrderResponse,
)
def update_print_order_status(
    order_id: int,
    status_data: PrintOrderStatusUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
):
    order = db.get(PrintOrder, order_id)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ на печать не найден",
        )

    order.status = status_data.status.value

    if "admin_comment" in status_data.model_fields_set:
        order.admin_comment = status_data.admin_comment

    try:
        db.commit()

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось изменить статус заказа",
        )

    return get_order_with_items(order_id, db)
