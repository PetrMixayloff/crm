from typing import Optional, List, Union
import datetime
from pydantic import BaseModel
from uuid import UUID
from .client import ClientCreate


class OrdersRawRelationBase(BaseModel):
    order_id: Optional[Union[UUID, str]] = None
    product_id: Union[UUID, str]
    raw_id: Union[UUID, str]
    standard_id: Union[UUID, str]
    quantity: int


class OrdersRawRelationCreate(OrdersRawRelationBase):
    pass


class OrdersRawRelationUpdate(OrdersRawRelationBase):
    id: str


class OrdersRawRelationInDBBase(OrdersRawRelationBase):
    id: UUID

    class Config:
        orm_mode = True


class OrdersRawRelation(OrdersRawRelationInDBBase):
    pass


class OrdersProductsRelationBase(BaseModel):
    product_id: Union[UUID, str]
    order_id: Optional[Union[UUID, str]] = None
    quantity: int
    raw: Optional[List[OrdersRawRelation]] = []


class OrdersProductsRelationCreate(OrdersProductsRelationBase):
    pass


class OrdersProductsRelationUpdate(OrdersProductsRelationBase):
    id: str


class OrdersProductsRelationInDBBase(OrdersProductsRelationBase):
    id: UUID

    class Config:
        orm_mode = True


class OrdersProductsRelation(OrdersProductsRelationInDBBase):
    pass


# Shared properties
class OrderBase(BaseModel):
    order_number: Optional[int] = None
    created_by_id: Union[UUID, str]
    make_by_id: Optional[Union[UUID, str]] = None
    shop_id: Union[UUID, str]
    client_id: Optional[Union[UUID, str]] = None
    client: Optional[ClientCreate] = None
    products: List[OrdersProductsRelation]
    delivery: bool
    courier_id: Optional[Union[UUID, str]] = None
    total_cost: float
    prepay: Optional[float] = 0
    prepay_type: str
    amount: float
    amount_type: str
    discount: Optional[float] = 0
    rating: Optional[int] = None
    status: str
    date_created: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_order: Optional[datetime.datetime]


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: str


class OrderInDBBase(OrderBase):
    id: UUID

    class Config:
        orm_mode = True


class Order(OrderInDBBase):
    pass
