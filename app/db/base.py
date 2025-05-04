from sqlalchemy import (
    create_engine,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)

engine = create_engine('sqlite:///shop.db', echo=True)

class Base(DeclarativeBase):
    ...

Session = sessionmaker(engine)

def create_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)