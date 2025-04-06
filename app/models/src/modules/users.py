from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from models.src.models import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, default="")
    phone: Mapped[str] = mapped_column(String, nullable=False, default="")
    sale: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    address: Mapped[str] = mapped_column(String, nullable=False, default="")

    def __repr__(self) -> str:
        return f"<User id={self.id}>"
