import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from .local_settings import LocalSettings
from .production_settings import ProductionSettings
from .base_settings import Settings


# --- Environment Selector Factory ---
def get_settings() -> Settings:
    # Read APP_ENV from system environment variables; defaults to 'local'
    env = os.getenv("APP_ENV", "local").lower()

    if env == "production":
        return ProductionSettings()
    return LocalSettings()


SETTINGS = get_settings()
