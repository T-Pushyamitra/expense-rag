
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    app_description: str
    app_port: int

    ollama_api_embedding_service_url: str
    vector_database_url: str

    metadata_host: str
    metadata_port: int
    metadata_database: str
    metadata_user: str
    metadata_password: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
