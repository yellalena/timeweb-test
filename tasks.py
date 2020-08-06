import logging

from furl import furl

from app import app
from celery_config import make_celery
from initialize import transaction
from models.task import Task
from web_parser.web_parser import WebParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

celery = make_celery(app)
local_parser = WebParser()

@celery.task()
def parse_data(task_id: str):
    try:
        with transaction as tx:
            task_info = Task.get_by_field(tx, uuid=task_id)
            local_parser.parse(furl(task_info.source), task_id)
            logger.debug(f"Parsed data {task_id}")
            # pack to ZIP
            # send somewhere, retrieve link
            # save link
    except Exception as e:
        pass