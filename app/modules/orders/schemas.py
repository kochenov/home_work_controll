from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    created_ad: datetime
    status: str


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    status: str


class OrderUpdate(BaseModel):
    status: str


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True
