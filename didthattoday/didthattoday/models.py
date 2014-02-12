from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()
Base.Session = DBSession

def json_me(instance):
    d = {}
    for attr in instance.json_attrs:
        d[attr] = getattr(instance, attr)
    return d

class Habit(Base):
    __tablename__ = 'habits'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)

    json_attrs = ['id', 'name', 'description']
    def to_json(self):
        return json_me(self)


class Step(Base):
    __tablename__ = 'steps'
    id = Column(Integer, primary_key=True)
    comment = Column(Text)
    happened_at = Column(DateTime, default=datetime.now, nullable=False)

    habit_id = Column(Integer, ForeignKey('habits.id'))
    habit = relationship(Habit)

    json_attrs = ['id', 'comment', 'habit_id']
    def to_json(self):
        return json_me(self)

