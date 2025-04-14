from typing import Any

from models.src.modules.orders import Order
from models.src.repository import BaseRepository


def get_search_row_Orders(
    query: Any,
    search_data: dict[str, Any] | None,
) -> Any:
    if search_data:
        if "is_paid" in search_data:
            query = query.where(Order.is_paid == search_data["is_paid"])

    return query


def get_ordering_Orders(
    self: Any,
    query: Any,
    value: str | list[str | list[str]] | None,
    search_data: dict[str, Any] | None = None,
) -> Any:
    if value is None:
        query = query.order_by(Order.id.desc())
    elif isinstance(value, list):
        for item in value:
            if item == "id__asc":
                query = query.order_by(Order.id.asc())
            elif item == "id__desc":
                query = query.order_by(Order.id.desc())

            elif item == "user_id__asc":
                query = query.order_by(Order.user_id.asc())
            elif item == "user_id__desc":
                query = query.order_by(Order.user_id.desc())

            elif item == "created_at__asc":
                query = query.order_by(Order.created_at.asc())
            elif item == "created_at__desc":
                query = query.order_by(Order.created_at.desc())

            elif item == "price__asc":
                query = query.order_by(Order.price.asc())
            elif item == "price__desc":
                query = query.order_by(Order.price.desc())

            elif item == "sale__asc":
                query = query.order_by(Order.sale.asc())
            elif item == "sale__desc":
                query = query.order_by(Order.sale.desc())

            elif item == "is_paid__asc":
                query = query.order_by(Order.is_paid.asc())
            elif item == "is_paid__desc":
                query = query.order_by(Order.is_paid.desc())

    return query


class OrderRepository(BaseRepository[Order]):
    def ordering(
        self,
        query: Any,
        value: str | list[str | list[str]] | None,
        search_data: dict[str, Any] | None = None,
    ) -> Any:
        return get_ordering_Orders(self, query, value, search_data)


Order_repository = OrderRepository(Order)
