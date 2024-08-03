from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

from app.core.database.database import BaseModel


class Product(BaseModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

    orders = relationship("Order", back_populates="product")
