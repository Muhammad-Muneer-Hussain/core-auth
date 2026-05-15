from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, RedisDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "CORE-AUTH"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://test_user:test_password@localhost:5432/core_auth_test"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    ACCESS_SECRET: str = "super_secret_access_key_change_me"
    REFRESH_SECRET: str = "super_secret_refresh_key_change_me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
