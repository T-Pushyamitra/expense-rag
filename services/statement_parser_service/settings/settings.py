import os

from .base_settings import Settings
from .local_settings import LocalSettings
from .production_settings import ProductionSettings


# --- Environment Selector Factory ---
def get_settings() -> Settings:
    # Read APP_ENV from system environment variables; defaults to 'local'
    env = os.getenv("APP_ENV", "local").lower()
    
    if env == "production":
        return ProductionSettings()
    return LocalSettings()

SETTINGS = get_settings()