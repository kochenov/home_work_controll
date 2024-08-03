from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    hashed_password: str


# Пример схемы обновления пользователя
class UpdateUser(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
