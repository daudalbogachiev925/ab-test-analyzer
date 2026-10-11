from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/abtest"
    DEFAULT_ALPHA: float = 0.05
    DEFAULT_POWER: float = 0.80
    BAYES_SAMPLES: int = 20000
    class Config:
        env_file = ".env"

settings = Settings()
