from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: str = 'INFO'
    ca_database_url: str

    cdsapi_url: str = 'https://cds.climate.copernicus.eu/api'
    cdsapi_key: str = None

    model_config = SettingsConfigDict(env_file='.env')  # dead: disable


class FeatureFlags(BaseSettings):
    temporal_downscaling: bool = False

    model_config = SettingsConfigDict(env_file='.env.feature')  # dead: disable
