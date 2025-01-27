from copy import deepcopy
from datetime import date, datetime
from typing import Annotated

from fastapi import status
from pydantic import (
    BaseModel, BeforeValidator, ConfigDict, Field, PositiveInt)

from app.core.schemas import (
    CustomerSchema,
    DefaultAPIResponse,
    default_responses,
    OrderSchema,
    SupplierSchema
)
from app.utils.work_with_dates import parse_like_date


class WarehouseInventoryBase(BaseModel):
    order_id: PositiveInt
    supplier_id: PositiveInt
    customer_id: PositiveInt
    quantity: PositiveInt
    price: PositiveInt
    order_date: datetime


class WarehouseInventoryCreate(BaseModel):
    order: Annotated[str, Field(min_length=3)]
    supplier: Annotated[str, Field(min_length=3)]
    customer: Annotated[str, Field(min_length=3)]
    quantity: PositiveInt
    price: PositiveInt
    order_date: Annotated[
        date,
        Field(examples=[datetime.now().strftime("%d.%m.%Y")]),
        BeforeValidator(
            lambda value: value if isinstance(value, (date, datetime))
            else parse_like_date(value))]


class WarehouseInventorySchema(WarehouseInventoryCreate):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    order: OrderSchema
    supplier: SupplierSchema
    customer: CustomerSchema


warehouse_inventory_create_response_example = DefaultAPIResponse(
    http_code=201,
    message="Warehouse inventory created successfully",
    data=WarehouseInventorySchema(
        id=1,
        order=OrderSchema(id=1, title="Order 1"),
        supplier=SupplierSchema(id=1, name="Supplier 1"),
        customer=CustomerSchema(id=1, name="Customer 1"),
        quantity=1,
        price=100,
        order_date=datetime.now().date()
    )
)


total_expenses_response_example = deepcopy(default_responses)
(
    total_expenses_response_example
    [status.HTTP_200_OK]["content"]["application/json"]["example"]
) = (
    DefaultAPIResponse(
        message="Total expenses calculated successfully",
        data={"total_expenses": 10000})
).model_dump()

add_new_warehouse_inventory_to_queue_response_example = (
    deepcopy(default_responses)
)
(
    add_new_warehouse_inventory_to_queue_response_example
    [status.HTTP_200_OK]["content"]["application/json"]["example"]
) = (
    DefaultAPIResponse(
        message=(
            "Warehouse inventory creating request "
            "added to queue successfully"))).model_dump()
