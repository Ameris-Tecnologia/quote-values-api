"""Module test fast-api"""

from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI, Security
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from fastapi_jsonapi import init
from modules.auth import VerifyToken

from database_connection import SQLA_ECHO, SQLA_URI, SQLA_USER_NAME, SQLA_PASS
from extensions.sql_session import Base
from urls import add_routes
from settings import Settings

settings = Settings()
auth = VerifyToken()
ambient = settings.ENV


async def sqlalchemy_init() -> AsyncEngine:
    """Function that connect database"""
    preffix_uri = 'mysql+asyncmy://'
    full_sql_uri = f'{preffix_uri}{SQLA_USER_NAME}:{SQLA_PASS}@{SQLA_URI}:3306/quote_values'
    uri_sql = full_sql_uri.strip()
    engine = create_async_engine(url=uri_sql, echo=SQLA_ECHO)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


@asynccontextmanager
async def lifespan(fapp: FastAPI):
    """Async function to fast-api connect to data-base"""
    fapp.state.async_session = await sqlalchemy_init()
    yield
    await fapp.state.async_session.dispose()


def create_app() -> FastAPI:
    """
    Create app factory.

    :return: app
    """

    app_scope = FastAPI(
        title="FastAPI and SQLAlchemy in DEV",
        debug=True,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    if ambient != "DEV":
        app_scope = FastAPI(
            title="FastAPI and SQLAlchemy in PROD",
            debug=False,
            openapi_url=None,
            docs_url=None,
            redoc_url=None,
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
def read_root(auth_result: str = Security(auth.verify)):
    """A valid access token is required to access this route"""
    return auth_result


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )
