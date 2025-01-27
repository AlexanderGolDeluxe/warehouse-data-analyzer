from app.core.schemas.base import DefaultAPIResponse, default_responses
from app.core.schemas.customer import CustomerCreate, CustomerSchema
from app.core.schemas.order import OrderCreate, OrderSchema
from app.core.schemas.supplier import SupplierCreate, SupplierSchema
from app.core.schemas.warehouse_inventory import (
    WarehouseInventoryBase,
    WarehouseInventoryCreate,
    WarehouseInventorySchema)
