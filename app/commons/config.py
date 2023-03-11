from pathlib import Path
from pydantic import BaseSettings, PostgresDsn, Field, validator
from sqlalchemy.engine.url import URL

BASEDIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str
    POSTGRES_HOST: str = Field(default="postgres")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_ECHO: bool = False
    POSTGRES_URL: PostgresDsn = None
    POSTGRES_URL_ASYNC: PostgresDsn = None
    SECRET_KEY: str
    ACCESS_TOKEN_HOURS_EXPIRE: int | None = 1
    JWT_ALGORITHM: str = Field(default="HS256")
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_HEADERS: list[str] = ["*"]
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = BASEDIR.parent / '.env'
        env_file_encoding = "UTF-8"

    @validator("POSTGRES_URL", always=True)
    def validate_db_url(cls, value: str | None, values):
        if value is None:
            return build_db_url(values=values)
        return value

    @validator("POSTGRES_URL_ASYNC", always=True)
    def validate_db_url_async(cls, value: str | None, values):
        if value is None:
            return build_db_url(values=values, async_db=True)
        return value


def build_db_url(values: dict[str, str | int | bool], async_db: bool = False):
    driver = "postgresql"
    if async_db:
        driver += "+asyncpg"
    return URL.create(
        drivername=driver,
        username=values["POSTGRES_USERNAME"],
        password=values["POSTGRES_PASSWORD"],
        database=values["POSTGRES_DATABASE"],
        host=values["POSTGRES_HOST"],
        port=values["POSTGRES_PORT"],
    )


settings = Settings()
