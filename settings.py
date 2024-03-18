"""Module for settings of env vars"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Class for settings of env vars"""
    # SANITY_API_KEY: str
    API_KEY: str
    API_KEY_NAME: str = "Authorization"
    ENV: str
    AWS_SECRETS_ACCESS_KEY: str
    AWS_SECRETS_ACCESS_KEY_ID: str
    PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT: int
    # ALLOWED_HOST: [str] = ["localhost", "127.0.0.1", "airtable.com"],
