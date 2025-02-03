from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    resend_api_key: str
    resend_domain: str
    resend_sender_name: str
    resend_sender: str

    max_size_file: int = 5 * 1024 * 1024


settings = Settings()
