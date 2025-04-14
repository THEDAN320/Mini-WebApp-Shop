from datetime import UTC, datetime
from typing import Any

from models.src.modules.users import User
from models.src.models import Base
from sqlalchemy import TIMESTAMP, Boolean, Float, ForeignKey, Integer, case
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, unique=False
    )
    price: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    sale: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    is_paid: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )
    is_closed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="f"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    user: Mapped[User] = relationship(User, lazy="selectin")

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
            (cls.sale == 0, cls.price), else_=cls.price * (1 - cls.sale / 100)
        )

    def __repr__(self) -> str:
        return f"<Order id={self.id}>"
