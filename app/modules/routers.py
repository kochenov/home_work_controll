from fastapi import APIRouter
from app.modules.users.router import router as user_routers
from app.modules.orders.router import router as order_routers
from app.modules.products.router import router as product_routers


routers = APIRouter()

routers.include_router(user_routers, prefix="/users", tags=["Пользователи"])
routers.include_router(order_routers, prefix="/orders", tags=["Заказы"])
routers.include_router(product_routers, prefix="/products", tags=["Товары"])

