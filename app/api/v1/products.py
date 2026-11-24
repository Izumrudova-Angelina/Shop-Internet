from fastapi import APIRouter, HTTPException, status
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductNotFoundError, product_service

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("", response_model=list[ProductRead])
async def list_products():
    return product_service.list_products()

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int):
    try:
        return product_service.get_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductCreate):
    return product_service.create_product(data)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, data: ProductUpdate):
    try:
        return product_service.update_product(product_id, data)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    try:
        product_service.delete_product(product_id)
    except ProductNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))