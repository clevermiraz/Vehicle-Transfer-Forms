from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND_DIR / ".env", extra="ignore")

    database_url: str
    secret_key: str
    access_token_minutes: int = 12 * 60
    cors_origins: list[str] = ["http://localhost:3000"]
    cookie_secure: bool = False
    # Original PDF forms. Read-only: the generator never writes to this directory.
    templates_dir: Path = PROJECT_DIR / "reference_forms"


settings = Settings()
