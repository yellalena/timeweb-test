import os
from contextlib import contextmanager

from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.task import create_all, drop_all

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
app.app_context().push()
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
if os.environ.get("DROP_DB", False):
    drop_all(engine)
create_all(engine)
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
api = Api(app)


@contextmanager
def transaction():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
