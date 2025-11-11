from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ca_database_url: str

    cdsapi_url: str = 'https://cds.climate.copernicus.eu/api'
    cdsapi_key: str

    model_config = SettingsConfigDict(env_file='.env')  # dead: disable
