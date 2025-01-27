from copy import deepcopy
from datetime import datetime
from typing import Annotated

from fastapi import status
from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.core.schemas import DefaultAPIResponse, default_responses


class OrderCreate(BaseModel):
    title: Annotated[str, Field(min_length=3)]


class OrderSchema(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt


most_popular_orders_response_example = deepcopy(default_responses)
(
    most_popular_orders_response_example
    [status.HTTP_200_OK]["content"]["application/json"]["example"]
) = (
    DefaultAPIResponse(
        message="Most popular orders finded successfully",
        data={
            "most_popular_orders": [{
                "order_id": 1,
                "title": "Order 1",
                "quantity": 10,
                "order_date": datetime.now()
            }]
        })).model_dump()
