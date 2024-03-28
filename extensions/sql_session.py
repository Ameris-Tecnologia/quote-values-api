"""Module base and metada"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database_connection import SQLA_URI, SQLA_ECHO, SQLA_USER_NAME, SQLA_PASS

Base = declarative_base()


def async_session() -> sessionmaker:
    """Function async session"""
    preffix_uri = 'mysql+asyncmy://'
    full_sql_uri = f'{preffix_uri}{SQLA_USER_NAME}:{SQLA_PASS}@{SQLA_URI}:3306/quote_values'
    uri_sql = full_sql_uri.strip()
    engine = create_async_engine(url=uri_sql, echo=SQLA_ECHO)
    _async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False)
    return _async_session


class Connector:
    """Class connector session."""
    @classmethod
    async def get_session(cls):
        """
        Get session as dependency

        :return:
        """
        sess = async_session()
        async with sess() as db_session:
            yield db_session
            await db_session.rollback()
