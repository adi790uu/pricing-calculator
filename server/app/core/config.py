import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str
    APP_NAME: str
    API_PREFIX: str = "/api"
    HOST_URL: str


class DevelopmentSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.development")


class TestSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.test")


class ProductionSettings(Settings):
    model_config = SettingsConfigDict(env_file=".env.production")


def get_settings() -> Settings:
    if os.getenv("APP_ENV", "development") == "production":
        return ProductionSettings()
    elif os.getenv("APP_ENV", "development") == "test":
        return TestSettings()
    else:
        return DevelopmentSettings()


settings = get_settings()
