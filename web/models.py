from uuid import uuid4

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

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

    from_url = Column(String(23), primary_key=True, index=True)
    to_url = Column(String, nullable=False)
    times_accessed = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    created_by = Column(ForeignKey("users.uuid"), nullable=False)

    user = relationship("User", backref="redirects")

    def __repr__(self):
        return '<Redirect from {from_url} to {to_url}>'.format(
            from_url=self.from_url,
            to_url=self.to_url
        )


class User(Base):
    __tablename__ = 'users'

    uuid = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    oauth_token = Column(String, nullable=False)
    oauth_secret = Column(String, nullable=False)

    def __repr__(self):
        return '<User {name}>'.format(name=self.name)

    def __init__(self, name):
        self.uuid = uuid4()
        self.name = name
        self.oauth_token = 'NA'
        self.oauth_secret = 'NA'
