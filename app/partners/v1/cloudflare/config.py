from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str
    public_url: str
    event_bucket_name: str = "event"
    avatar_folder_name: str = "user-avatars"


settings = Settings()
