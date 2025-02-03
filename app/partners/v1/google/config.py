from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    client_id_google: str
    client_secret_google: str
    redirect_uri_google: str


settings = Settings()
