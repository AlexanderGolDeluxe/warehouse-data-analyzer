from datetime import timedelta

from loguru import logger
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Order, WarehouseInventory
from app.core.schemas import OrderCreate, OrderSchema
from app.utils.work_with_dates import parse_like_date


@logger.catch(reraise=True)
async def create_order(session: AsyncSession, order_in: OrderCreate):
    order = Order(**order_in.model_dump())
    session.add(order)
    await session.commit()

    return OrderSchema.model_validate(order)


@logger.catch(reraise=True)
async def bulk_create_orders(
        session: AsyncSession, orders_in: list[OrderCreate]
    ):
    new_orders = await session.scalars(
        insert(Order).returning(Order), orders_in
    )
    await session.commit()

    return [
        OrderSchema.model_validate(order) for order in new_orders.all()]


@logger.catch(reraise=True)
async def get_most_popular_orders_by_qty(
        session: AsyncSession,
        from_order_date: str | None = None,
        to_order_date: str | None = None,
        limit: int | None = None
    ):
    stmt = (
        select(
            Order.id.label("order_id"),
            Order.title,
            WarehouseInventory.quantity,
            WarehouseInventory.order_date
        )
        .join(WarehouseInventory)
    )
    if from_order_date is not None:
        stmt = stmt.where(
            WarehouseInventory.order_date >=
            parse_like_date(from_order_date))

    if to_order_date is not None:
        stmt = stmt.where(
            WarehouseInventory.order_date <
            parse_like_date(to_order_date) + timedelta(days=1))

    most_popular_orders = await session.execute(
        stmt.order_by(WarehouseInventory.quantity.desc()).limit(limit)
    )
    most_popular_orders = map(
        lambda row: {key: value for key, value in row.items()},
        most_popular_orders.mappings())

    return dict(most_popular_orders=list(most_popular_orders))
