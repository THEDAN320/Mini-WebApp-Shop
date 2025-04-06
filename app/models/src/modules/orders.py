from datetime import datetime, UTC
from typing import Any
from sqlalchemy import Boolean, DateTime, Float, Integer, ForeignKey, case
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from models.src.modules.users import User
from models.src.modules.orders_goods import OrderGoods
from models.src.models import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, unique=True
    )
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    sale: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    is_paid: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    user: Mapped[User] = relationship(User, lazy="selectin")
    order_goods: Mapped[list[OrderGoods]] = relationship(lazy="selectin")

    @hybrid_property
    def price_with_sale(self) -> float:
        """Calculate price with sale."""
        if self.sale == 0:
            return self.price
        return self.price * (1 - self.sale / 100)

    @price_with_sale.expression  # type: ignore
    def price_with_sale(cls) -> Any:
        """SQL expression for price with sale calculation."""
        return case(
            (cls.sale == 0, cls.price),
            else_=cls.price * (1 - cls.sale / 100)
        )

    def __repr__(self) -> str:
        return f"<Order id={self.id}>"
