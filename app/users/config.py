from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    default_admin_email: str
    default_admin_password: str
    minimum_length_of_the_password: int = Field(default=8)
    maximum_avatar_file_size: int = Field(default=5 * 1024 * 1024)  # default 5MB


settings = Settings()
