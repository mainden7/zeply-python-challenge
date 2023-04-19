from typing import Any

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import PostgresDsn
from pydantic import validator

load_dotenv()


class PostgresDsnCustom(PostgresDsn):
    """Custom postgres schemes to allow asyncpg driver in pydantic builder."""

    allowed_schemes = {"postgres", "postgresql", "postgresql+asyncpg"}


class Settings(BaseSettings):
    """Main project settings.

    Automatically loads and assigns to corresponding variables
    all private settings from .env file.
    """

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    CRYPT_SCHEMA: str = "argon2"

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    BACKEND_CORS_ORIGINS: str | list[str] | None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str) -> list[str]:
        """
        Convert string with origins to list.

        Example:
            "http://localhost, http://localhost:8080"
            -> ["http://localhost", "http://localhost:8080"]
        """
        return list(map(lambda x: x.strip(), v.split(",")))

    POSTGRES_SERVER: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None
    SQLALCHEMY_ASYNC_DATABASE_URI: PostgresDsnCustom | None
    SQLALCHEMY_ECHO: bool = True

    @validator("SQLALCHEMY_DATABASE_URI", pre=True, always=True)
    def assemble_db_connection(
        cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        """
        Return database DSN.

        This DSN string is combined from individual database settings that
        are in the .env configuration file. Return SQLALCHEMY_DATABASE_URI
        variable value if it is set explicitly

        Args:
            v: Postgres DSN like
            postgresql+psycopg2://user:password@host:port/db_name

            values: A dict containing all variables loaded from .env file

        Returns: A DSN string
        """
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @validator("SQLALCHEMY_ASYNC_DATABASE_URI", pre=True, always=True)
    def assemble_db_connection_async(
        cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        """Return database DSN for asynchronous calls.

        This DSN string is combined from individual database settings that
        are in the .env configuration file. Return SQLALCHEMY_DATABASE_URI
        variable value if it is set explicitly

        Args:
            v: Postgres DSN like
            postgresql+asyncpg://user:password@host:port/db_name

            values: A dict containing all variables loaded from .env file

        Returns: A DSN string
        """
        if isinstance(v, str):
            return v
        # TODO: Change to pydantic builder after they release new
        #  version with support of async scheme
        return PostgresDsnCustom.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # wallet settings
    WALLET_ENTROPY_STRENGTH: int
    WALLET_MNEMONIC_PHRASE_LANGUAGE: str

    # other settings
    MAX_ENTITIES_PER_PAGE: int = 20
    HASH_SALT: str

    class Config:  # noqa: D106
        case_sensitive = True


settings = Settings()
