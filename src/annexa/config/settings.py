from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://annexa:password@127.0.0.1:5432/annexa_dev"

    jwt_secret: str = "super_secret_dev_key_change_me_in_production"
    jwt_algorithm: str = "HS256"
    jwt_access_expiration_minutes: int = 15

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
