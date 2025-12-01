from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import quote_plus


class Settings(BaseSettings):
    """Application settings and configuration"""

    # Database credentials
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "apexdata_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # FastF1
    FASTF1_CACHE_DIR: str = "./fastf1_cache"

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "ApexData API"
    VERSION: str = "1.0.0"

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:3001"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL with properly encoded password"""
        return f"postgresql://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
