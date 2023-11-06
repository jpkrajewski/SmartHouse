import os
from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_SDN: str = ""
    CELERY_BROKER_URL: str = "redis://:password123@localhost:6379/0"
    CELERY_BACKEND_URL: str = "sqlite+aiosqlite:///fastapi.db"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    STORAGE_LOCAL_PATH: Path = Path(Path(__file__).parent.parent, "storage")
    MQTT_NAMESPACE: str = "smarthouse"


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = "mysql+aiomysql://root:fastapi@db:3306/fastapi"
    READER_DB_URL: str = "mysql+aiomysql://root:fastapi@db:3306/fastapi"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = "sqlite+aiosqlite:///fastapi.db"
    READER_DB_URL: str = "sqlite+aiosqlite:///fastapi.db"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"
    READER_DB_URL: str = "mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
