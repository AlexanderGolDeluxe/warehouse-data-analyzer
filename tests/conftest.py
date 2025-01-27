from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient

from app import create_app
from app.config import BASE_DIR, DB_URL
from app.configuration.db_helper import DatabaseHelper, db_helper
from app.configuration.rmq_helper import rmq_helper
from app.core.models import Base
from app.utils.fake_inventory_creator import (
    create_fake_warehouse_inventories)

DB_NAME_TEST = "test_db"
DB_URL_TEST = DB_URL.replace(
    f"{BASE_DIR.stem}.sqlite3", f"{DB_NAME_TEST}.sqlite3")

db_test = DatabaseHelper(DB_URL_TEST)

test_orders = [
    dict(
        order="Order 1",
        supplier="Supplier 1",
        customer="Customer 1",
        quantity=10,
        price=100,
        order_date="24.01.2025"
    ),
    dict(
        order="Order 2",
        supplier="Supplier 2",
        customer="Customer 2",
        quantity=10000,
        price=1000000,
        order_date="25.01.2025"
    )
]


async def manage_db_models_test(is_create: bool):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(
            Base.metadata.create_all if is_create
            else Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    await manage_db_models_test(True)
    session = db_test.get_scoped_session()
    await create_fake_warehouse_inventories(session)
    await rmq_helper.init_connect()

    yield

    await rmq_helper.close_connect()
    await session.close()
    await manage_db_models_test(False)
    await db_test.engine.dispose()


app = create_app()
app.dependency_overrides[db_helper.scoped_session_dependency] = (
    db_test.scoped_session_dependency)

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test"
        ) as ac:
        yield ac
