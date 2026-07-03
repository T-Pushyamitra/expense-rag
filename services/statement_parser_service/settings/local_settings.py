from .base_settings import Settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class LocalSettings(Settings):
    debug: bool = True
    
    model_config = {
                        **Settings.model_config,
                        "env_file": BASE_DIR / ".env",
            }
