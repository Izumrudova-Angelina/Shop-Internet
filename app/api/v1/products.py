from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductNotFoundError, ProductService

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=list[ProductRead], summary="Список товаров")
async def list_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.list_products()

@router.get("/{product_id}", response_model=ProductRead, summary="Получить товар")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    try:
        return await service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED, summary="Создать товар")
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.create_product(data)

@router.put("/{product_id}", response_model=ProductRead, summary="Обновить товар")
async def update_product(product_id: int, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    try:
        return await service.update_product(product_id, data)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить товар")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    try:
        await service.delete_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))