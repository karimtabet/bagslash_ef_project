from datetime import datetime

from sqlalchemy import Column, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Index
from uuid import uuid4

convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Redirect(Base):

    __tablename__ = 'redirects'

    redirect_uuid = Column(UUID(as_uuid=True), primary_key=True)
    from_url = Column(String, nullable=False)
    to_url = Column(String, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, from_url, to_url):
        self.redirect_uuid = uuid4
        self.from_url = from_url
        self.to_url = to_url
        self.date_posted = datetime.datetime.now()

    def __repr__(self):
        return '<Redirect from {from_url} to {to_url}>'.format(
            from_url=self.from_url,
            to_url=self.to_url
        )
