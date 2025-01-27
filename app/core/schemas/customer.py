from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class CustomerCreate(BaseModel):
    name: Annotated[str, Field(min_length=3)]


class CustomerSchema(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
