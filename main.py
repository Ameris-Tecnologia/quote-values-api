"""Module test fast-api"""

from contextlib import asynccontextmanager

import uvicorn

from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from fastapi_jsonapi import init


from config import SQLA_ECHO, SQLA_URI, SQLA_USER_NAME, SQLA_PASS
from extensions.sql_session import Base
from urls import add_routes, settings, get_api_key


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
