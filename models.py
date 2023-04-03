from cachetools import cached
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import Integer, Column, String

import config


Base = declarative_base()


class SwapiPeople(Base):

    __tablename__ = 'swapi_people'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String)
    eye_color = Column(String)
    films = Column(String)
    gender = Column(String)
    hair_color = Column(String)
    height = Column(String)
    homeworld = Column(String)
    mass = Column(String)
    name = Column(String)
    skin_color = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)


@cached({})
def get_engine():
    return create_async_engine(config.PG_DSN)

@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine(), class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with get_engine().begin() as con:
        await con.run_sync(Base.metadata.create_all)

def close_db():
    get_engine().dispose()

