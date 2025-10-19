from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(table_name)s__%(column_0_name)s",
        "uq": "uq_%(table_name)s__%(column_0_name)s",
        "ck": "ck_%(table_name)s__%(constraint_name)s",
        "fk": "fk_%(table_name)s__%(column_0_name)s__%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(DeclarativeBase):
    metadata = metadata
