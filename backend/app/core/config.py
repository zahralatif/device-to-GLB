from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    HOST: str
    PORT: int

    STORAGE_PATH: str
    UPLOAD_PATH: str

    DATABASE_URL: str

    AGGLOGIC_BASE_URL: str = ""
    AGGLOGIC_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()