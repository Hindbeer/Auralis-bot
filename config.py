from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    BOT_TOKEN: str
    ADMIN_ID: int
    TELEGRAM_CHANNEL_ID: str
    BOT_LINK: str
    HOST_URL: str

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
