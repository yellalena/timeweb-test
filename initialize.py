import os
from contextlib import contextmanager

from flask import Flask
from flask_restful import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from celery_config import make_celery
from models.task import create_all, drop_all

app = Flask(__name__)
app.config["SECRET_KEY"] = "super secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql+psycopg2://test:test@localhost:5432/timeweb_test")
app.config["CELERY_BROKER_URL"] = os.getenv("CELERY_BROKER_URL", 'amqp://myuser:mypassword@localhost:5672//')
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
if os.environ.get("DROP_DB", False):
    drop_all(engine)
create_all(engine)
Session = scoped_session(sessionmaker(expire_on_commit=False))
Session.configure(bind=engine)
celery = make_celery(app)
api = Api(app)
app.app_context().push()


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
