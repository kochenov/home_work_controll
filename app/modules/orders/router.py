from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from starlette import status

from .repository import OrderRepository
from .schemas import Order, OrderCreate, OrderUpdate

router = APIRouter()

disable_installed_extensions_check()


@router.get("/", name="Получить список заказов")
async def read_orders() -> Page[Order]:
    try:
        orders = await OrderRepository.get_all()
        if not orders:
            raise ValueError("В базе данных нет записей")
        return paginate(orders)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.post("/add", name="Добавление заказа")
async def add_order(order_data: OrderCreate = Depends()) -> dict:
    """
    Добавление нового заказа


    :param order_data: данные для записи
    :return: dict
    """
    try:
        await OrderRepository.create(**order_data.model_dump())
        return {"message": "Запись успешно создана", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.put("/edit/{order_id}", name="Обновить данные товара")
async def update_order(order_id: int, order_update: OrderUpdate = Depends()):
    """
    Обновить данные ссылки по ID.
    """
    order = await OrderRepository.get_one(id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    await OrderRepository.update(order_id, **order_update.model_dump())
    return {"message": "Запись успешно обновлена"}


@router.delete("/delete/{id_order}", name="Удаление пользователя")
async def delete_order(id_order: int):
    """
    Удаление записи


    :param id_order: данные для записи
    :return: dict
    """
    try:
        # получаем товар по ID из базы данных
        order = await OrderRepository.get_one(id=id_order)
        # если такой товар существует в БД
        if not order:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такой товар не существует")
        #
        await OrderRepository.delete(id=id_order)
        return {"message": "Запись успешно удалена", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
