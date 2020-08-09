import logging

import requests
from furl import furl

from application.data_processor import DataProcessor
from initialize import transaction, celery
from models import TaskNotFound
from models.task import Task, TaskStatus

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

processor = DataProcessor()


@celery.task(bind=True, max_retries=3)
def parse_data(self, task_id: str):
    try:
        with transaction() as tx:
            task_info = Task.get_by_field(tx, uuid=task_id)
            if not task_info:
                raise TaskNotFound
            link = processor.consume_url(furl(task_info.source), task_id)
            task_info.result = link
            task_info.status = TaskStatus.done
            task_info.save(tx)
            logger.debug("Successfully processed data for task %s", task_id)
    except TaskNotFound:
        logger.error("Could not find task %s.", task_id)
        raise
    except requests.exceptions.ConnectionError as e:
            logger.warning("Connection error. Retrying.")
            self.retry(countdown=2 ** self.request.retries, exc=e)
    except Exception as e:
        with transaction() as tx:
            task = Task.get_by_field(tx, uuid=task_id)
            task.status = TaskStatus.error
            logger.error("Failed to parse data due to unexpected error. %s", str(e))
        raise