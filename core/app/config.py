from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    model_config = SettingsConfigDict(env_file=".env")

    SECRET_KEY: str = "my-secret-key"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
