from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import Base


class Customer(Base):
    __tablename__ = "customer"

    name: Mapped[str] = mapped_column(unique=True)
