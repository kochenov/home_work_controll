from fastapi import APIRouter, HTTPException, Depends
from fastapi_pagination import Page, paginate
from fastapi_pagination.utils import disable_installed_extensions_check
from starlette import status

from app.modules.users.schemas import User, UserCreate, UpdateUser
from .repository import UserRepository

router = APIRouter()

disable_installed_extensions_check()


@router.get("/", name="Получить список пользователей")
async def read_users() -> Page[User]:
    # Получить список пользователей
    try:
        users = await UserRepository.get_all()
        if not users:
            raise ValueError("В базе данных нет записей")
        return paginate(users)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{str(e)}"
        )


@router.post("/add", name="Добавление нового пользователя")
async def add_user(user_data: UserCreate = Depends()) -> dict:
    """
    Создание нового пользователя в БД


    :param user_data: данные для записи
    :return: dict
    """
    try:
        # получаем ссылку из базы данных
        user = await UserRepository.get_one(email=user_data.email)
        # если такой пользователь существует в БД
        if user:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такой пользователь уже существует")
        # если ссылке в БД нет, то делаем новую запись
        await UserRepository.create(**user_data.model_dump())
        return {"message": "Запись успешно создана", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.put("/edit/{user_id}", name="Обновить пользователя")
async def update_user(user_id: int, user_update: UpdateUser = Depends()):
    """
    Обновить данные ссылки по ID.
    """
    user = await UserRepository.get_one(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await UserRepository.update(user_id, **user_update.model_dump())
    return {"message": "Запись успешно обновлена"}


@router.delete("/delete/{id_user}", name="Удаление пользователя")
async def delete_user(id_user: int):
    """
    Удаление записи об объявлении


    :param id_user: данные для записи
    :return: dict
    """
    try:
        # получаем пользователя по ID из базы данных
        user = await UserRepository.get_one(id=id_user)
        # если такой пользователь существует в БД
        if not user:
            # выводим ошибку 500 с пояснением
            raise HTTPException(status_code=500, detail="Такой пользователь не существует")
        #
        await UserRepository.delete(id=id_user)
        return {"message": "Запись успешно удалена", "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
