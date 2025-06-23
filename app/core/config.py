from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field   # Field continua no pydantic “principal”

class Settings(BaseSettings):
    mongo_uri: str = Field("mongodb://localhost:27018", env="MONGO_URI")
    mongo_db: str = Field("tabular_api", env="MONGO_DB_NAME")
    postgres_uri: str = Field(
        "postgresql+asyncpg://user:pass@db:5432/tabular_api", env="POSTGRES_URI"
    )
    backend: str = Field("mongo", env="BACKEND")  # mongo | postgres

    # diz onde está o .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache
def get_settings() -> Settings:
    return Settings()