from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Bot settings loaded from environment variables.

    This class handles all configuration settings for the Telegram bot
    and service URLs.

    Attributes:
        BOT_TOKEN: Telegram bot token from @BotFather
        BACKEND_URL: URL for the backend service
    """

    # Bot settings
    BOT_TOKEN: str = ""

    # Backend URLs
    BACKEND_URL: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        env_file=[".env", ".env_dev"],
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )


@lru_cache
def get_bot_settings() -> BotSettings:
    """Get cached bot settings instance.

    Returns:
        BotSettings: Cached settings instance
    """
    settings = BotSettings()
    print(">>> Loading bot settings")
    return settings
