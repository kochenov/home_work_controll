from sqlalchemy import select

from app.core.database.base_repository import BaseRepository
from app.core.database.database import async_session_maker
from .models import Order


class OrderRepository(BaseRepository):
    model = Order
