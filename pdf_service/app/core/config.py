from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"


settings = Settings()
