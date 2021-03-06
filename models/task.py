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
        current_session.flush()

    @classmethod
    def get_by_field(cls, current_session, **kwargs):
        return current_session.query(cls).filter_by(**kwargs).first()