from hashlib import sha1
from datetime import datetime
import os

from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    Table,
    Sequence,
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
    userid = Column(Integer, ForeignKey('users.id'), nullable=False)

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

def groupfinder(userid, request):
    user = User.from_id(userid)
    return [g.name for g in user.groups]

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer,
                   Sequence('groups_seq_id', optional=True),
                   primary_key=True)
    name = Column(Text, unique=True)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,
                   Sequence('users_seq_id', optional=True),
                   primary_key=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    groups = relationship(Group, secondary='user_group')
    habits = relationship(Habit)

    def __init__(self, login, password, groups=[]):
        self.login = login
        self._set_password(password)
        self.groups = groups

    @classmethod
    def from_id(cls, userid):
        return cls.Session.query(User).filter(User.id==userid).first()

    @classmethod
    def from_login(cls, login):
        return cls.Session.query(User).filter(User.login==login).first()

    def _set_password(self, password):
        hashed_password = password

        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()

        if not isinstance(hashed_password, unicode):
            hashed_password = hashed_password.decode('UTF-8')

        self.password = hashed_password

    def validate_password(self, password):
        hashed_pass = sha1()
        hashed_pass.update(password + self.password[:40])
        return self.password[40:] == hashed_pass.hexdigest()

user_group_table = Table('user_group', Base.metadata,
    Column('user_id', Integer, ForeignKey(User.id)),
    Column('group_id', Integer, ForeignKey(Group.id)),
)
