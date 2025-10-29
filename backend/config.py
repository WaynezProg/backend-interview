from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 資料庫設定
    database_url: str = "sqlite:///./social_platform.db"
    
    # JWT 設定
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # 應用程式設定
    app_name: str = "Social Platform API"
    debug: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
