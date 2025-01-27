from loguru import logger
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import Customer
from app.core.schemas import CustomerCreate, CustomerSchema


@logger.catch(reraise=True)
async def find_customers_by_name(
        session: AsyncSession, customer_names: list[str]
    ):
    finded_customers = await session.scalars(
        select(Customer).where(func.lower(Customer.name).in_(
            map(str.lower, customer_names))))

    return [
        CustomerSchema.model_validate(customer)
        for customer in finded_customers.all()]


@logger.catch(reraise=True)
async def get_or_create_customer(
        session: AsyncSession, customer_name: str
    ):
    stmt = select(Customer).where(
        func.lower(Customer.name) == customer_name.lower()
    )
    customer = await session.scalar(stmt)
    if customer is None:
        customer = Customer(name=customer_name)
        session.add(customer)
        await session.commit()

    return CustomerSchema.model_validate(customer)


@logger.catch(reraise=True)
async def bulk_create_customers(
        session: AsyncSession, customers_in: list[CustomerCreate]
    ):
    customer_items = dict()
    customer_name_values = list()
    for customer_in in customers_in:
        customer_items[customer_in.name] = None
        customer_name_values.append(dict(name=customer_in.name))

    new_customers = await session.scalars(
        sqlite_insert(Customer).values(customer_name_values)
        .on_conflict_do_nothing(index_elements=[Customer.name])
        .returning(Customer)
    )
    await session.commit()
    customer_items.update({
        created_customer.name: CustomerSchema.model_validate(
            created_customer
        )
        for created_customer in new_customers.all()
    })
    existing_customers = [
        customer_item_name for customer_item_name, customer_item
        in customer_items.items() if customer_item is None
    ]
    if existing_customers:
        customer_items.update({
            finded_customer.name: finded_customer
            for finded_customer in await find_customers_by_name(
                session, existing_customers)})

    return customer_items
