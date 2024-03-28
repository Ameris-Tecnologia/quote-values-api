"""Module to access dict with configurations"""
from modules.aws_handler import get_secret_from_str

secrets = get_secret_from_str(secret_name="quote-values-database")

SQLA_URI = secrets["SQLA_URI"]
SQLA_ECHO = secrets["SQLA_ECHO"] == "1"
SQLA_USER_NAME = secrets["SQLA_USER_NAME"]
SQLA_PASS = secrets["SQLA_PASS"]
