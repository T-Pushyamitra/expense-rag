import os

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_description: str
    app_port: int
    
    embedding_service_url: str
    database_url: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

