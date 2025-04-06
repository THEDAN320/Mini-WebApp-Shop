from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.src.models import Base, TimestampMixin


class Good(Base, TimestampMixin):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<Good id={self.id}>"
