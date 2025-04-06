from functools import lru_cache

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class BackendSettings(BaseSettings):
    """Backend settings loaded from environment variables.

    This class handles all configuration settings for the
    database connection details.

    Attributes:
        POSTGRES_DB: PostgreSQL database name
        POSTGRES_USER: Database user
        POSTGRES_PASSWORD: Database password
        POSTGRES_HOST: Database host
        POSTGRES_PORT: Database port
        DATABASE_URL: Constructed database URL (optional)
    """

    # Database settings
    POSTGRES_DB: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_HOST: str | None = None
    POSTGRES_PORT: int | None = None
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
        result = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=values.get('POSTGRES_DB'),
        )
        return str(result)

    model_config = SettingsConfigDict(
        env_file=[".env", ".env_dev"],
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
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
