"""Module test fast-api"""

import json
from contextlib import asynccontextmanager

import uvicorn

from fastapi import Depends, FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader, APIKey
from sqlalchemy.ext.asyncio import create_async_engine

from fastapi_jsonapi import init


from modules.aws_handler import AWS
from settings import Settings
from config import secret_name, SQLA_ECHO, SQLA_URI, SQLA_USER_NAME, SQLA_PASS
from extensions.sql_session import Base
from urls import add_routes

settings = Settings()
secrets = json.loads(AWS.get_secret(
    AWS.create_session_secretsmanager(), secret_name[settings.ENV]))
AUTHORIZATION_TOKEN = secrets["TOKEN_API_MONOLITH"]

API_KEY = settings.API_KEY
API_KEY_NAME = settings.API_KEY_NAME
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(
    api_key: str = Security(api_key_header),
):
    """Async function to get api key"""
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403)


async def sqlalchemy_init() -> None:
    """Function that connect database"""
    preffix_uri = 'mysql+asyncmy://'
    full_sql_uri = f'{preffix_uri}{SQLA_USER_NAME}:{SQLA_PASS}@{SQLA_URI}:3306/quote_values'
    uri_sql = full_sql_uri.strip()
    engine = create_async_engine(url=uri_sql, echo=SQLA_ECHO)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(fapp: FastAPI):
    """Async function to fast-api connect to data-base"""
    fapp.state.async_session = await sqlalchemy_init()
    yield
    await fapp.state.async_session.session.close()
    await fapp.state.async_session.session.engine.dispose()


def create_app() -> FastAPI:
    """
    Create app factory.

    :return: app
    """
    app_scope = FastAPI(
        title="FastAPI and SQLAlchemy",
        debug=True,
        openapi_url="/openapi.json",
        docs_url="/docs",
        lifespan=lifespan
    )
    add_routes(app_scope)
    init(app_scope)
    return app_scope


app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )


@app.get("/")
def read_root(
    _: APIKey = Depends(get_api_key),
):
    """Function that read root"""
    return f"Hello from {settings.ENV}"


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )
