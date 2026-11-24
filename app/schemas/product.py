from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class ProductStatus(str, Enum):
    AVAILABLE = "available"
    OUT_OF_STOCK = "out_of_stock"
    ARCHIVED = "archived"

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Название")
    description: str | None = Field(None, max_length=2000, description="Описание")
    price: Decimal = Field(..., gt=0, description="Цена")
    category: str = Field(..., min_length=1, max_length=100, description="Категория")
    stock: int = Field(0, ge=0, description="Количество")
    status: ProductStatus = Field(ProductStatus.AVAILABLE)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=2000)
    price: Decimal | None = Field(None, gt=0)
    category: str | None = Field(None, min_length=1, max_length=100)
    stock: int | None = Field(None, ge=0)
    status: ProductStatus | None = None

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime