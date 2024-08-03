from fastapi import FastAPI  # Импорт FastAPI для создания приложения
from fastapi.routing import APIRoute  # Импорт класса APIRoute для работы с маршрутами
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware  # Импорт CORSMiddleware для обработки CORS

from app.core.config.config import settings  # Импорт настроек из модуля app.core.settings
from app.modules.routers import routers  # Импорт маршрутов из модуля app.modules.routers


def custom_generate_unique_id(route: APIRoute) -> str:
    """
    Функция для создания уникальных идентификаторов маршрутов.

    Args:
        route: Объект маршрута (APIRoute).

    Returns:
        Строка, сформированная из первой метки (tag) и названия маршрута,
        разделенных дефисом.
    """
    return f"{route.tags[0]}-{route.name}"


# Создание экземпляра приложения FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,  # Заголовок приложения из настроек
    openapi_url=f"{settings.API_V1_STR}/openapi.json",  # URL документации OpenAPI
    generate_unique_id_function=custom_generate_unique_id,  # Функция для уникальных ID маршрутов
)

# Включение CORS middleware (при наличии разрешенных доменов в настройках)
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
        allow_headers=["*"],
    )

# Подключение маршрутов из модуля routers с префиксом из настроек
app.include_router(routers, prefix=settings.API_V1_STR)

# Добавление пагинации
add_pagination(app)
