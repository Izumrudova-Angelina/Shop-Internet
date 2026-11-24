from datetime import datetime, timezone
from itertools import count
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead, ProductStatus

class ProductNotFoundError(Exception):
    pass

class ProductService:
    def __init__(self) -> None:
        self._storage: dict[int, ProductRead] = {}
        self._id_counter = count(start=1)

    def list_products(self) -> list[ProductRead]:
        return list(self._storage.values())

    def get_product(self, product_id: int) -> ProductRead:
        product = self._storage.get(product_id)
        if not product:
            raise ProductNotFoundError(f"Product with id={product_id} not found")
        return product

    def create_product(self, data: ProductCreate) -> ProductRead:
        now = datetime.now(timezone.utc)
        product = ProductRead(id=next(self._id_counter), created_at=now, updated_at=now, **data.model_dump())
        self._storage[product.id] = product
        return product

    def update_product(self, product_id: int, data: ProductUpdate) -> ProductRead:
        existing = self.get_product(product_id)
        updated = existing.model_copy(update={**data.model_dump(exclude_unset=True), "updated_at": datetime.now(timezone.utc)})
        self._storage[product_id] = updated
        return updated

    def delete_product(self, product_id: int) -> None:
        if product_id not in self._storage:
            raise ProductNotFoundError(f"Product with id={product_id} not found")
        del self._storage[product_id]

product_service = ProductService()