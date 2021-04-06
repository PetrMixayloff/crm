from typing import Optional, List, Union
from datetime import datetime, timezone
from pydantic import BaseModel
from uuid import UUID
from .client import ClientCreate, ClientUpdate, Client


class OrdersProductsRawRelationBase(BaseModel):
    order_product_id: Optional[Union[UUID, str]] = None
    raw_id: Union[UUID, str]
    image: Optional[str] = None
    standard_id: Optional[Union[UUID, str]] = None
    quantity: int


class OrdersProductsRawRelationCreate(OrdersProductsRawRelationBase):
    pass


class OrdersProductsRawRelationUpdate(OrdersProductsRawRelationBase):
    id: str


class OrdersProductsRawRelationInDBBase(OrdersProductsRawRelationBase):
    id: UUID

    class Config:
        orm_mode = True


class OrdersProductsRawRelation(OrdersProductsRawRelationInDBBase):
    pass


class OrdersProductsRelationBase(BaseModel):
    product_id: Union[UUID, str]
    order_id: Optional[Union[UUID, str]] = None
    image: Optional[str] = None
    quantity: int
    price: float


class OrdersProductsRelationCreate(OrdersProductsRelationBase):
    raw: Optional[List[OrdersProductsRawRelationCreate]] = []


class OrdersProductsRelationUpdate(OrdersProductsRelationBase):
    id: str
    raw: Optional[List[Union[OrdersProductsRawRelationUpdate, OrdersProductsRawRelationCreate]]] = []


class OrdersProductsRelationInDBBase(OrdersProductsRelationBase):
    id: UUID
    raw: Optional[List[OrdersProductsRawRelation]] = []

    class Config:
        orm_mode = True


class OrdersProductsRelation(OrdersProductsRelationInDBBase):
    pass


# Shared properties
class OrderBase(BaseModel):
    order_number: Optional[int] = None
    make_by_id: Optional[Union[UUID, str]] = None
    client_id: Optional[Union[UUID, str]] = None
    shop_id: Union[UUID, str]
    delivery: bool
    courier_id: Optional[Union[UUID, str]] = None
    total_cost: float
    prepay: Optional[float] = 0
    prepay_type: str
    amount: float
    amount_type: Optional[str] = None
    discount: Optional[float] = 0
    rating: Optional[int] = None
    status: str
    date_created: Optional[datetime] = datetime.utcnow()
    date_of_order: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        }


class OrderCreate(OrderBase):
    created_by_id: Optional[UUID] = None
    client: Optional[ClientCreate] = None
    products: Optional[List[OrdersProductsRelationCreate]] = []


class OrderUpdate(OrderBase):
    id: str
    created_by_id: str
    client: Optional[ClientUpdate] = None
    products: Optional[List[Union[OrdersProductsRelationUpdate, OrdersProductsRelationCreate]]] = []


class OrderInDBBase(OrderBase):
    id: UUID
    created_by_id: UUID
    client: Optional[Client] = None
    products: List[OrdersProductsRelation]

    class Config:
        orm_mode = True


class Order(OrderInDBBase):
    pass
