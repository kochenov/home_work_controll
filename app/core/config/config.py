import secrets  # Импорт для генерации секретного ключа
import warnings  # Импорт для вывода предупреждений

from typing import (  # Импорт для аннотации типов
    Annotated,
    Any,
    Literal,
)

from pydantic import (  # Импорт для объявления схемы конфигурации
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
)

from pydantic_core import MultiHostUrl  # Импорт для построения мультихостового URL
from pydantic_settings import BaseSettings, SettingsConfigDict  # Импорт для объявления базового класса настроек
from typing_extensions import Self  # Импорт для использования типа Self


def parse_cors(v: Any) -> list[str] | str:
    """
    Парсит значение CORS из строки или списка в список разрешенных доменов.

    Args:
        v: Значение CORS для парсинга (строка или список).

    Returns:
        Список разрешенных доменов CORS.

    Raises:
        ValueError: Если значение CORS не является строкой или списком.
    """

    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """
    Класс конфигурации приложения.

    Наследуется от BaseSettings для объявления схемы конфигурации.
    Использует SettingsConfigDict для настройки чтения из файла .env.
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    API_V1_STR: str = "/api/v1"  # Версия API (строка)
    SECRET_KEY: str = secrets.token_urlsafe(32)  # Секретный ключ (генерируется автоматически)
    REDIS_HOST: str = 'localhost'

    # Время жизни токена доступа в минутах (8 дней)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    DOMAIN: str = "localhost"  # Домен приложения
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"  # Окружение (local, staging, production)

    @computed_field  # Поле, вычисляемое автоматически
    @property
    def server_host(self) -> str:
        """
        Возвращает хост сервера с учетом окружения (http/https).

        Returns:
            Строка с хостом сервера (http://localhost или https://localhost)
        """

        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []  # Разрешенные CORS-домены (список или строка)

    PROJECT_NAME: str  # Название проекта
    SENTRY_DSN: HttpUrl | None = None  # DSN для Sentry (необязательный)

    POSTGRES_SERVER: str  # Хост базы данных PostgreSQL
    POSTGRES_PORT: int = 5432  # Порт базы данных PostgreSQL
    POSTGRES_USER: str  # Пользователь базы данных PostgreSQL
    POSTGRES_PASSWORD: str  # Пароль пользователя базы данных PostgreSQL
    POSTGRES_DB: str = ""  # База данных PostgreSQL

    @computed_field  # Поле, вычисляемое автоматически
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Возвращает строку подключения к базе данных PostgreSQL.

        Returns:
            Строка подключения к базе данных PostgreSQL.
        """

        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore