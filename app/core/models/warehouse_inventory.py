from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models import Base

if TYPE_CHECKING:
    from app.core.models import Customer, Order, Supplier

class WarehouseInventory(Base):
    __tablename__ = "warehouse_inventory"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    order: Mapped["Order"] = relationship(
        back_populates="warehouse_inventories"
    )
    supplier_id: Mapped[int] = mapped_column(ForeignKey("supplier.id"))
    supplier: Mapped["Supplier"] = relationship()
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped["Customer"] = relationship()
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")
    price: Mapped[int] = mapped_column(CheckConstraint("price > 0"))
    order_date: Mapped[datetime]
