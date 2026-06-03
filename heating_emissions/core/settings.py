from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    log_level: str = 'INFO'

    data_db_host: str
    data_db_port: int
    data_db_name: str
    data_db_user: str
    data_db_password: str

    cdsapi_url: str = 'https://cds.climate.copernicus.eu/api'
    cdsapi_key: str = None

    model_config = SettingsConfigDict(env_file='.env')  # dead: disable

    @property
    def ca_database_url(self) -> str:
        return f'postgresql://{self.data_db_user}:{self.data_db_password}@{self.data_db_host}:{self.data_db_port}/{self.data_db_name}'


class FeatureFlags(BaseSettings):
    temporal_downscaling: bool = False

    model_config = SettingsConfigDict(env_file='.env.feature')  # dead: disable
