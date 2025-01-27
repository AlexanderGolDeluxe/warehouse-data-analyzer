from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Supplier, WarehouseInventory
from app.core.schemas import SupplierCreate, SupplierSchema


@logger.catch(reraise=True)
async def get_or_create_supplier(
        session: AsyncSession, supplier_name: str
    ):
    stmt = select(Supplier).where(
        func.lower(Supplier.name) == supplier_name.lower()
    )
    supplier = await session.scalar(stmt)
    if supplier is None:
        supplier = Supplier(name=supplier_name)
        session.add(supplier)
        await session.commit()

    return SupplierSchema.model_validate(supplier)


@logger.catch(reraise=True)
async def find_top_supplier_by_orders(session: AsyncSession, limit: int):
    stmt = (
        select(
            Supplier.id.label("supplier_id"),
            Supplier.name,
            func.count(WarehouseInventory.id).label("orders_count")
        )
        .join(WarehouseInventory)
        .group_by(Supplier.id)
        .order_by(func.count(WarehouseInventory.id).desc())
        .limit(limit)
    )
    top_supplier_by_orders = await session.execute(stmt)
    top_supplier_by_orders = map(
        lambda row: {key: value for key, value in row.items()},
        top_supplier_by_orders.mappings())

    return dict(top_supplier_by_orders=list(top_supplier_by_orders))


@logger.catch(reraise=True)
async def find_suppliers_by_name(
        session: AsyncSession, supplier_names: list[str]
    ):
    finded_suppliers = await session.scalars(
        select(Supplier).where(func.lower(Supplier.name).in_(
            map(str.lower, supplier_names))))

    return [
        SupplierSchema.model_validate(supplier)
        for supplier in finded_suppliers.all()]


@logger.catch(reraise=True)
async def bulk_create_suppliers(
        session: AsyncSession, suppliers_in: list[SupplierCreate]
    ):
    supplier_items = dict()
    supplier_name_values = list()
    for supplier_in in suppliers_in:
        supplier_items[supplier_in.name] = None
        supplier_name_values.append(dict(name=supplier_in.name))

    new_suppliers = await session.scalars(
        sqlite_insert(Supplier).values(supplier_name_values)
        .on_conflict_do_nothing(index_elements=[Supplier.name])
        .returning(Supplier)
    )
    await session.commit()
    supplier_items.update({
        created_supplier.name: SupplierSchema.model_validate(
            created_supplier
        )
        for created_supplier in new_suppliers.all()
    })
    existing_suppliers = [
        supplier_item_name for supplier_item_name, supplier_item
        in supplier_items.items() if supplier_item is None
    ]
    if existing_suppliers:
        supplier_items.update({
            finded_supplier.name: finded_supplier
            for finded_supplier in await find_suppliers_by_name(
                session, existing_suppliers)})

    return supplier_items
