from enum import Enum

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def create_all(engine):
    Base.metadata.create_all(bind=engine)


def drop_all(engine):
    Base.metadata.drop_all(bind=engine)


class TaskStatus(str, Enum):
    accepted = "accepted"
    processing = "processing"
    done = "done"
    error = "error"


class Task(Base):
    __tablename__ = "parser_tasks"

    id = sql.Column(sql.Integer, primary_key=True)
    uuid = sql.Column(sql.String)
    source = sql.Column(sql.String)
    result = sql.Column(sql.String)
    status = sql.Column(sql.Enum(TaskStatus))

    def __repr__(self):
        return f"<Task(uuid={self.uuid}, source: {self.source}, status: {self.status}. {self.result}>"

    def save(self, current_session):
        current_session.add(self)

    @classmethod
    def get_by_id(cls, current_session, id):
        return current_session.query(cls).filter_by(id=id).first()

    @classmethod
    def show_all(cls, current_session):
        return current_session.query(cls).all()

    @classmethod
    def find_by_field(cls, current_session, **kwargs):
        return current_session.query(cls).filter_by(**kwargs).all()

    @classmethod
    def get_by_field(cls, current_session, **kwargs):
        return current_session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def find_first(cls, current_session, **kwargs):
        return current_session.query(cls).filter_by(**kwargs).first()

    @classmethod
    def find_one(cls, current_session, **kwargs):
        return current_session.query(cls).filter_by(**kwargs).one()
