from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
