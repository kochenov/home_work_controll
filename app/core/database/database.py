import datetime
from typing import AsyncGenerator

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from app.core.config.config import settings

# Конфигурирование асинхронного движка SQLAlchemy для взаимодействия с базой данных
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# Фабрика для создания асинхронных сессий базы данных.
# Сессия - это объект, который олицетворяет собой разговор с базой данных.
# Она предоставляет методы для выполнения запросов, добавления, обновления и удаления данных.
async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


# Базовая модель для сущностей (таблиц) базы данных
class BaseModel(DeclarativeBase):
    __abstract__ = True  # Абстрактный класс служит основой для создания конкретных моделей

    # Автоматическое формирование названия таблицы на основе имени класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"  # Название в нижнем регистре с суффиксом "s"

    # Первичный ключ таблицы (столбец, однозначно идентифицирующий каждую запись)
    id: Mapped[int] = mapped_column(primary_key=True)
    created_ad = Column(DateTime, default=datetime.datetime.now())
    update_ad = Column(DateTime, nullable=True, default=None)


# Асинхронная функция для получения сессии базы данных
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    # Создание асинхронного контекстного менеджера для сессии с помощью фабрики
    async with async_session_maker() as session:
        # Возврат сессии в качестве асинхронного генератора
        yield session
