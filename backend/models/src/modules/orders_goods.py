from models.src.modules.goods import Good
from models.src.modules.orders import Order
from models.src.models import Base, TimestampMixin
from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderGoods(Base, TimestampMixin):
    __tablename__ = "orders_goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id"), nullable=False
    )
    good_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("goods.id"), nullable=False
    )
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    order: Mapped[Order] = relationship(Order, lazy="selectin")
    good: Mapped[Good] = relationship(Good, lazy="selectin")

    def __repr__(self) -> str:
        return f"<OrderGood id={self.id}>"
