from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from starlette import status

from .repository import ProductRepository
from .schemas import Product, ProductCreate

router = APIRouter()

disable_installed_extensions_check()


@router.get("/", name="Получить список товаров")
async def read_products() -> Page[Product]:
    try:
        products = await ProductRepository.get_all()
        if not products:
            raise ValueError("В базе данных нет записей")
        return paginate(products)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.post("/add", name="Добавление нового товара")
async def add_product(product_data: ProductCreate = Depends()) -> dict:
    """
    Добавление нового товара


    :param product_data: данные для записи
    :return: dict
    """
    try:
        # добавляем в БД
        product = await ProductRepository.get_one(name=product_data.name)
        if product:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такой товар уже существует")
        # если товар в БД нет, то делаем новую запись
        await ProductRepository.create(**product_data.model_dump())
        return {"message": "Запись успешно создана", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.put("/edit/{product_id}", name="Обновить данные товара")
async def update_product(product_id: int, product_update: Product = Depends()):
    """
    Обновить данные ссылки по ID.
    """
    product = await ProductRepository.get_one(id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")

    await ProductRepository.update(product_id, **product_update.model_dump())
    return {"message": "Запись успешно обновлена"}


@router.delete("/delete/{id_product}", name="Удаление пользователя")
async def delete_product(id_product: int):
    """
    Удаление записи


    :param id_product: данные для записи
    :return: dict
    """
    try:
        # получаем товар по ID из базы данных
        product = await ProductRepository.get_one(id=id_product)
        # если такой товар существует в БД
        if not product:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такой товар не существует")
        #
        await ProductRepository.delete(id=id_product)
        return {"message": "Запись успешно удалена", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
