from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str
    error_webhook_url: str


settings = Settings()
