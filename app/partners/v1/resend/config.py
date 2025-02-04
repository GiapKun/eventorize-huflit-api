from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    resend_api_key: Optional[str] = None
    host_email: str = Field(default="noreply@giapkun.site")
    sender_name: str = Field(default="Eventorize")
    verification_link: str = Field(default="https://seoer.top/verify-email?token=")
    reset_password_link: str = Field(default="https://seoer.top/reset-password?token=")

settings = Settings()
