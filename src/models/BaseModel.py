from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from configs.Database import Engine


# Base Entity Model Schema
EntityMeta = declarative_base()


def init():
    EntityMeta.metadata.create_all(bind=Engine)  # type: ignore


class BaseModel(EntityMeta):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )
