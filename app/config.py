from functools import lru_cache
from typing import cast

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendSettings(BaseSettings):
    """Backend settings loaded from environment variables.

    This class handles all configuration settings for the
    database connection details.

    Attributes:
        DB_NAME: PostgreSQL database name
        DB_USER: Database user
        DB_PASS: Database password
        DB_HOST: Database host
        DB_PORT: Database port
        DATABASE_URL: Constructed database URL (optional)
    """

    # Database settings
    DB_NAME: str | None = None
    DB_USER: str | None = None
    DB_PASS: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL")
    def get_database_url(cls, v: str | None, info: ValidationInfo) -> str:
        """Construct database URL from individual components if not provided.

        Args:
            v: Existing database URL if provided
            info: Validation context containing other settings

        Returns:
            Constructed PostgreSQL database URL
        """
        if isinstance(v, str) and v:
            return v
        values = info.data
        result = cast(
            str,
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.get("DB_USER"),
                password=values.get("DB_PASS"),
                host=values.get("DB_HOST"),
                port=values.get("DB_PORT"),
                path=f"/{values.get('DB_NAME')}",
            ),
        )
        return result

    model_config = SettingsConfigDict(
        env_file=[".env", ".env_dev"],
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_backend_settings() -> BackendSettings:
    """Get cached backend settings instance.

    Returns:
        BackendSettings: Cached settings instance
    """
    settings = BackendSettings()
    print(">>> Loading backend settings")
    return settings
