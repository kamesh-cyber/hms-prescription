from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Database settings
    DB_HOST: str = "mysql"
    DB_PORT: int = 3306
    DB_USER: str = "prescription_user"
    DB_PASSWORD: str = "prescription_pass"
    DB_NAME: str = "prescription_db"

    # Application settings
    APP_NAME: str = "Prescription Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

