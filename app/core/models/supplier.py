from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class Supplier(Base):
    __tablename__ = "supplier"

    name: Mapped[str] = mapped_column(unique=True)
