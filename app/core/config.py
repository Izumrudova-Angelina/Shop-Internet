from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./shop.db"
    app_debug: bool = True
    app_secret_key: str = "super_secret_key_for_dev"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()