import aio_pika
from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import API_PREFIX, INVENTORY_CREATION_QUEUE_NAME
from app.configuration.rmq_helper import rmq_helper
from app.configuration.db_helper import db_helper
from app.core.crud.warehouse_inventory import (
    calculate_total_expenses, create_one_warehouse_inventory
)
from app.core.schemas import DefaultAPIResponse, WarehouseInventoryCreate
from app.core.schemas.warehouse_inventory import (
    add_new_warehouse_inventory_to_queue_response_example,
    total_expenses_response_example)

router = APIRouter(
    prefix=API_PREFIX + "/warehouse-inventory",
    tags=["Warehouse Inventory"])


@router.get("/total-expenses", responses=total_expenses_response_example)
async def get_total_expenses(
        from_order_date: str | None = None,
        to_order_date: str | None = None,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
    ):
    return DefaultAPIResponse(
        message="Total expenses calculated successfully",
        data=await calculate_total_expenses(
            session=session,
            from_order_date=from_order_date,
            to_order_date=to_order_date))


@router.post("/create", status_code=201, include_in_schema=False)
async def create_warehouse_inventory(
        warehouse_inventory_in: WarehouseInventoryCreate,
        session: AsyncSession = Depends(db_helper.get_scoped_session)
    ):
    return DefaultAPIResponse(
        http_code=201,
        message="Warehouse inventory created successfully",
        data=await create_one_warehouse_inventory(
            session=session,
            wh_inventories_in=warehouse_inventory_in))


@router.post(
    "/add",
    responses=add_new_warehouse_inventory_to_queue_response_example
)
async def add_warehouse_inventory(
        warehouse_inventory_in: WarehouseInventoryCreate,
        rmq_channel: aio_pika.robust_channel.RobustChannel = (
            Depends(rmq_helper.get_channel))
    ):
    confirm = await rmq_channel.default_exchange.publish(
        message=aio_pika.Message(
            body=warehouse_inventory_in.model_dump_json().encode(),
            delivery_mode=2
        ),
        routing_key=INVENTORY_CREATION_QUEUE_NAME
    )
    log_message = (
        "Warehouse inventory creating request "
        "added to queue successfully"
    )
    logger.info(log_message)
    return DefaultAPIResponse(message=log_message)
