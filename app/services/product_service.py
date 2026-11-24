from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead


class ProductNotFoundError(Exception):
    pass


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_products(self) -> list[ProductRead]:
        result = await self.session.execute(select(Product))
        products = result.scalars().all()
        return [ProductRead.model_validate(p) for p in products]

    async def get_product(self, product_id: int) -> ProductRead:
        product = await self.session.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(f"Product with id={product_id} not found")
        return ProductRead.model_validate(product)

    async def create_product(self, data: ProductCreate) -> ProductRead:
        product = Product(
            name=data.name,
            description=data.description,
            price=data.price,
            category=data.category,
            stock=data.stock,
            status=data.status.value
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return ProductRead.model_validate(product)

    async def update_product(self, product_id: int, data: ProductUpdate) -> ProductRead:
        product = await self.session.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(f"Product with id={product_id} not found")

        update_data = data.model_dump(exclude_unset=True)
        if "status" in update_data and update_data["status"]:
            update_data["status"] = update_data["status"].value

        for key, value in update_data.items():
            setattr(product, key, value)

        await self.session.commit()
        await self.session.refresh(product)
        return ProductRead.model_validate(product)

    async def delete_product(self, product_id: int) -> None:
        product = await self.session.get(Product, product_id)
        if not product:
            raise ProductNotFoundError(f"Product with id={product_id} not found")
        await self.session.delete(product)
        await self.session.commit()