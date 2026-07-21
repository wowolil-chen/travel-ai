from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Qwen
    QWEN_API_KEY: str
    QWEN_BASE_URL: str
    QWEN_MODEL: str

    # QWeather
    WEATHER_API_KEY: str
    WEATHER_HOST: str

    # AMap
    AMAP_API_KEY: str
    AMAP_BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()