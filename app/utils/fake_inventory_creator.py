from datetime import datetime, timedelta
from random import choice, choices, randint
from string import ascii_lowercase

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud.warehouse_inventory import (
    bulk_create_warehouse_inventories
)
from app.core.schemas import WarehouseInventoryCreate


@logger.catch
def get_random_name(length_name: int = 5):
    generated_name = (
        "".join(choices(ascii_lowercase + " ", k=length_name))
        .strip().capitalize()
    )
    if len(generated_name) < 3:
        generated_name = ("The " + generated_name).strip()

    return generated_name


@logger.catch
def get_random_order_date(max_date: datetime = datetime(2025, 12, 31)):
    return max_date - timedelta(days=randint(1, 1000))


@logger.catch
def generate_fake_names(amount_names: int = 100):
    return [
        get_random_name(randint(3, 100)) for _ in range(amount_names)
    ]


@logger.catch
def generate_fake_warehouse_inventory(
        fake_customers: list[str],
        fake_orders: list[str],
        fake_suppliers: list[str]
    ):
    return WarehouseInventoryCreate(
        customer=choice(fake_customers),
        order=choice(fake_orders),
        supplier=choice(fake_suppliers),
        quantity=randint(1, 100),
        price=randint(1, 10000),
        order_date=get_random_order_date())


@logger.catch
async def create_fake_warehouse_inventories(
        session: AsyncSession, amount_inventories: int = 10000
    ):
    fake_customers = generate_fake_names()
    fake_orders = generate_fake_names(amount_inventories)
    fake_suppliers = generate_fake_names()
    new_warehouse_inventories = await bulk_create_warehouse_inventories(
        session,
        [
            generate_fake_warehouse_inventory(
                fake_customers, fake_orders, fake_suppliers
            )
            for _ in range(amount_inventories)
        ]
    )
    if len(new_warehouse_inventories) == amount_inventories:
        logger.info("Fake warehouse inventories created successfully")
