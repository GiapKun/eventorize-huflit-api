from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_database_name: str
    database_url: str
    log_database_name: str


settings = Settings()
