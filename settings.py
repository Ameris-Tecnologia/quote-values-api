"""Module for settings of env vars"""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class for settings of env vars"""
    AWS_SECRETS_ACCESS_KEY: str
    AWS_SECRETS_ACCESS_KEY_ID: str
    ENV: str

    class Config:
        """Class for env variables"""
        env_file = "custom.env"


@lru_cache()
def get_settings():
    """Function for settings of env vars"""
    return Settings()
