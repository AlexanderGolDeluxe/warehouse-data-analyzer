from copy import deepcopy
from typing import Annotated

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.schemas import DefaultAPIResponse, default_responses


class SupplierCreate(BaseModel):
    name: Annotated[str, Field(min_length=3)]


class SupplierSchema(SupplierCreate):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt


top_suppliers_by_orders_response_example = deepcopy(default_responses)
(
    top_suppliers_by_orders_response_example
    [status.HTTP_200_OK]["content"]["application/json"]["example"]
) = (
    DefaultAPIResponse(
        message="Top suppliers by orders finded successfully",
        data={
            "top_supplier_by_orders": [{
                "supplier_id": 1,
                "name": "Supplier 1",
                "orders_count": 100
            }]
        })).model_dump()
