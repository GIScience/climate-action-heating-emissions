from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ca_database_url: str

    model_config = SettingsConfigDict(env_file='.env')  # dead: disable
