from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from app.core.models import Base

if TYPE_CHECKING:
    from app.core.models import WarehouseInventory


class Order(Base):
    __tablename__ = "order"

    title: Mapped[str]
    warehouse_inventories: Mapped[list["WarehouseInventory"]] = (
        relationship(back_populates="order"))
