from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    SERVER_PORT: int = 80
    SERVER_HOST: str = "0.0.0.0"

    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]

    # Options
    USE_STREAMS: bool = True

    # Database
    DATABASE_URI: str

    # External APIs
    PRODUCT_API: str


settings = Settings()
