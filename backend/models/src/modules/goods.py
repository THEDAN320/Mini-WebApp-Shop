from models.src.models import Base, TimestampMixin
from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Good(Base, TimestampMixin):
    __tablename__ = "goods"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    count: Mapped[int] = mapped_column(Integer, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False, default="")
    type: Mapped[str] = mapped_column(String, nullable=False, default="")
    description: Mapped[str] = mapped_column(
        String, nullable=False, default=""
    )

    def __repr__(self) -> str:
        return f"<Good id={self.id}>"
