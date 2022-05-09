import os
from typing import Any, Literal, cast

from dynaconf import Dynaconf
from pydantic import AnyHttpUrl, BaseModel, PositiveInt, RedisDsn, StrictBool, StrictStr


ENVIRONMENT = Literal['development', 'testing', 'production']
BASE_DIR = os.getcwd()


class AppConfiguration(BaseModel):
    title: StrictStr
    description: StrictStr


class CacheConfiguration(BaseModel):
    dsn: RedisDsn
    expire_minutes: PositiveInt


class DatabaseConfiguration(BaseModel):
    dsn: StrictStr


class ServerConfiguration(BaseModel):
    host: StrictStr
    port: PositiveInt


class CORSConfiguration(BaseModel):
    origins: list[AnyHttpUrl]


class JWTConfiguration(BaseModel):
    algorithm: StrictStr
    expire_hours: PositiveInt


class BaseSuperuser(BaseModel):
    username: StrictStr
    password: StrictStr
    email: StrictStr


class LocalizationConfiguration(BaseModel):
    fallback_locale: StrictStr
    available_locales: list[StrictStr]


class FileUploadConfiguration(BaseModel):
    max_size_mb: PositiveInt
    allowed_extensions: list[StrictStr]


class Configuration(BaseModel):
    app: AppConfiguration
    base_superuser: BaseSuperuser
    cache: CacheConfiguration
    cors: CORSConfiguration
    database: DatabaseConfiguration
    debug: StrictBool
    environment: StrictStr
    file_upload: FileUploadConfiguration
    jwt: JWTConfiguration
    localization: LocalizationConfiguration
    secret_key: StrictStr
    server: ServerConfiguration


def load_configuration(env: ENVIRONMENT | None = None) -> Configuration:
    if env is None:
        env = cast(ENVIRONMENT, os.getenv('DYNACONF_ENV', 'development'))

    settings = Dynaconf(
        settings_files=['default.yaml', f'{env}.yaml', '.secrets.yaml'],
        load_dotenv=True,
        merge_enabled=True,
        root_path=os.path.join(BASE_DIR, 'config'),
    )

    config: dict[str, Any] = {'environment': env}
    for key in Configuration.__fields__.keys():
        if settings.get(key) is not None:
            config[key] = settings[key]

    return Configuration(**config)
