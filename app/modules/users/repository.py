from sqlalchemy import select

from app.core.database.base_repository import BaseRepository
from app.core.database.database import async_session_maker
from .models import User


class UserRepository(BaseRepository):
    """Репозиторий для работы с пользователями.

    Предоставляет методы для:
        * Получения пользователей по различным критериям
        * Добавления новых пользователей
        * Обновления информации о пользователях
        * Удаление пользователя

    Пример использования:

    ```python
    from modules.users.repository import UserRepository

    # Получить список пользователей
    user_repository = UsersRepository()
    all_users = user_repository.get_all()

    # Добавить нового пользователя
    new_user = User(user_id=1, name="Roman", age=30)
    user_repository.add(new_user)

    # Обновить пользователя
    user_repository.update(user_id=1, name="Roman", age=30)

    # Удалить пользователя
    process_repository.delete(user_id=1)
    ```
    """

    model = User
