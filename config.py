"""Module to access dict with configurations"""
from os import getenv

SQLA_URI = getenv("SQLA_URI", "sqlite+aiosqlite:///./db.sqlite3")
SQLA_ECHO = getenv("SQLA_ECHO", "0") == "1"
SQLA_USER_NAME = getenv("SQLA_USER_NAME", "sqlite+aiosqlite:///./db.sqlite3")
SQLA_PASS = getenv("SQLA_PASS", "sqlite+aiosqlite:///./db.sqlite3")

secret_name = dict(
    development="claves-prod-monolith",
    production="claves-prod-monolith"
)
