import asyncio

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import (
    HANDLER_INVENTORY_CREATION_INTERVAL, INVENTORY_CREATION_QUEUE_NAME
)
from app.configuration.rmq_helper import rmq_helper
from app.core.crud.warehouse_inventory import (
    bulk_create_warehouse_inventories
)
from app.core.schemas import WarehouseInventoryCreate


@logger.catch
async def handle_inventory_creation(session: AsyncSession):
    queue_name = INVENTORY_CREATION_QUEUE_NAME
    queue = await rmq_helper.channel.declare_queue(
        queue_name, durable=True
    )
    while True:
        inventory_creation_messages = list()
        inventory_items_to_create = list()
        while True:
            message = await queue.get(fail=False)
            if message is None or len(inventory_creation_messages) > 10:
                break

            inventory_creation_messages.append(message)
            inventory_items_to_create.append(
                WarehouseInventoryCreate.model_validate_json(
                    message.body.decode()))

        if inventory_items_to_create:
            created_inventories = (
                await bulk_create_warehouse_inventories(
                    session, inventory_items_to_create)
            )
            if len(created_inventories) == len(inventory_items_to_create):
                await rmq_helper.ack_messages(
                    inventory_creation_messages
                )
                inventory_creation_messages = None
            else:
                await rmq_helper.nack_messages(
                    inventory_creation_messages)

        if inventory_creation_messages:
            rmq_helper.ack_messages(inventory_creation_messages)

        await asyncio.sleep(HANDLER_INVENTORY_CREATION_INTERVAL)
