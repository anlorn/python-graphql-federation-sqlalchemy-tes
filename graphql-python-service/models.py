from sqlalchemy import create_engine, Column, Integer, String, func, DateTime, Boolean
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


class Store(Base):
    __tablename__ = 'store'
    store_id = Column(String, primary_key=True)
    tenant = Column(String, primary_key=True)
    working_hours = Column(String)
    is_enabled = Column(Boolean)
    address = Column(String)


Base.metadata.create_all(engine)
