"""Module for settings of env vars"""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class for settings of env vars"""
    AUTH0_DOMAIN: str
    AUTH0_ALGORITHMS: str
    AUTH0_API_AUDIENCE: str
    AUTH0_ISSUER: str
    PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT: int

    class Config:
        """Class for env variables"""
        env_file = "custom.env"


@lru_cache()
def get_settings():
    """Function for settings of env vars"""
    return Settings()
