from pydantic_settings import BaseSettings, SettingsConfigDict
#from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    database_url : str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # model_config = SettingsConfigDict(env_file="client-followup-ai/.env", extra="ignore")
    # model_config = SettingsConfigDict(
    #     env_file=BASE_DIR / ".env",
    #     extra="ignore",
    # )
settings = Settings()