from datetime import timedelta

from loguru import logger
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud.customers import (
    bulk_create_customers, get_or_create_customer
)
from app.core.crud.orders import bulk_create_orders, create_order
from app.core.crud.suppliers import (
    bulk_create_suppliers, get_or_create_supplier
)
from app.core.models import WarehouseInventory
from app.core.schemas import (
    CustomerCreate,
    OrderCreate,
    SupplierCreate,
    WarehouseInventoryBase,
    WarehouseInventoryCreate,
    WarehouseInventorySchema
)
from app.utils.work_with_dates import parse_like_date


@logger.catch(reraise=True)
async def calculate_total_expenses(
        session: AsyncSession,
        from_order_date: str | None = None,
        to_order_date: str | None = None
    ):
    stmt = select(
        func.sum(WarehouseInventory.price * WarehouseInventory.quantity)
    )
    if from_order_date is not None:
        stmt = stmt.where(
            WarehouseInventory.order_date >=
            parse_like_date(from_order_date))

    if to_order_date is not None:
        stmt = stmt.where(
            WarehouseInventory.order_date <
            parse_like_date(to_order_date) + timedelta(days=1))

    return dict(total_expenses=await session.scalar(stmt))


@logger.catch(reraise=True)
async def create_one_warehouse_inventory(
        session: AsyncSession,
        wh_inventories_in: WarehouseInventoryCreate
    ):
    new_order = await create_order(
        session, OrderCreate(title=wh_inventories_in.order)
    )
    supplier_item = await get_or_create_supplier(
        session, wh_inventories_in.supplier
    )
    customer_item = await get_or_create_customer(
        session, wh_inventories_in.customer
    )
    new_wh_inventory_item = WarehouseInventoryBase(
        order_id=new_order.id,
        supplier_id=supplier_item.id,
        customer_id=customer_item.id,
        quantity=wh_inventories_in.quantity,
        price=wh_inventories_in.price,
        order_date=wh_inventories_in.order_date
    )
    new_wh_inventory = WarehouseInventory(
        **new_wh_inventory_item.model_dump()
    )
    session.add(new_wh_inventory)
    await session.commit()

    return dict(created_wh_inventory=WarehouseInventorySchema(
        order=new_order,
        supplier=supplier_item,
        customer=customer_item,
        **vars(new_wh_inventory)))


@logger.catch(reraise=True)
async def bulk_create_warehouse_inventories(
        session: AsyncSession,
        wh_inventories_in: list[WarehouseInventoryCreate]
    ):
    customers_to_create = list()
    orders_to_create = list()
    suppliers_to_create = list()
    for wh_inventory_in in wh_inventories_in:
        customers_to_create.append(
            CustomerCreate(name=wh_inventory_in.customer)
        )
        orders_to_create.append(
            OrderCreate(title=wh_inventory_in.order)
        )
        suppliers_to_create.append(
            SupplierCreate(name=wh_inventory_in.supplier))
    
    new_customers = await bulk_create_customers(
        session, customers_to_create
    )
    new_orders = await bulk_create_orders(session, orders_to_create)
    new_suppliers = await bulk_create_suppliers(
        session, suppliers_to_create
    )
    new_wh_inventories = await session.scalars(
        insert(WarehouseInventory).returning(WarehouseInventory),
        [
            WarehouseInventoryBase(
                customer_id=new_customers[wh_inventory_in.customer].id,
                order_id=new_order.id,
                supplier_id=new_suppliers[wh_inventory_in.supplier].id,
                quantity=wh_inventory_in.quantity,
                price=wh_inventory_in.price,
                order_date=wh_inventory_in.order_date
            )
            for new_order, wh_inventory_in in
            zip(new_orders, wh_inventories_in)
        ]
    )
    await session.commit()

    created_wh_inventories = [
        WarehouseInventorySchema(
            id=created_wh_inventory.id,
            customer=new_customers[wh_inventory_in.customer],
            order=new_order,
            supplier=new_suppliers[wh_inventory_in.supplier],
            quantity=created_wh_inventory.quantity,
            price=created_wh_inventory.price,
            order_date=created_wh_inventory.order_date.date()
        )
        for new_order, wh_inventory_in, created_wh_inventory in
        zip(new_orders, wh_inventories_in, new_wh_inventories.all())
    ]
    logger.info(
        f"{len(created_wh_inventories)} "
        "warehouse inventories created successfully")

    return created_wh_inventories
