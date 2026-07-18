from .base_settings import Settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class ProductionSettings(Settings):
    debug: bool = False

    model_config = {
        **Settings.model_config,
        "env_file": BASE_DIR / ".env.production",
    }
