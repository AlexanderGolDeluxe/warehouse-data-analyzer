import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.configuration.db_helper import db_helper
from app.configuration.rmq_helper import rmq_helper
from app.configuration.routes import __routes__
from app.core.models import Base
from app.utils.fake_inventory_creator import (
    create_fake_warehouse_inventories
)
from app.utils.inventory_creation_worker import handle_inventory_creation


class Server:

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_routes(app)

    def get_app(self):
        return self.__app

    @staticmethod
    def __register_routes(app: FastAPI):
        __routes__.register_routers(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session = db_helper.get_scoped_session()
    await create_fake_warehouse_inventories(session)
    await rmq_helper.init_connect()
    handle_inventory_creation_task = asyncio.create_task(
        handle_inventory_creation(session))

    yield

    handle_inventory_creation_task.cancel()
    await rmq_helper.close_connect()
    await session.close()
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await db_helper.engine.dispose()
