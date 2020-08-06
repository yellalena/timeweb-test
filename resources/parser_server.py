import logging
import uuid

from flask_restful import Resource
from flask import request

from initialize import transaction
from models.task import Task, TaskStatus
from resources import resp, err

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SiteParser(Resource):
    def post(self):
        try:
            with transaction() as tx:
                data = request.get_json()
                task_id = str(uuid.uuid4())
                new_task = Task(uuid=task_id,
                                source=data["url"],
                                status=TaskStatus.accepted)
                new_task.save(tx)
            import tasks
            tasks.parse_data.delay(task_id)
            logger.debug("Accepted a new task: %s", str(new_task))
            return resp("task_id",
                        task_id,
                        201)
        except Exception as e:
            logger.error("Something went wrong while adding a new task: %s", str(e))
            return err(f"Failed to add a new task: {str(e)}", 500)


class Result(Resource):
    def get(self, id: str):
        try:
            with transaction() as tx:
                task = Task.get_by_field(tx, uuid=id)
                if task.status == TaskStatus.done:
                    msg = {"url_to_download": task.result}
                else:
                    msg = {"task_status": task.status}
                return resp("result",
                            msg,
                            200)
        except Exception as e:
            logger.error("Something went wrong while getting info on task %s", id)
            return err(f"Failed to retrieve info on task {id}: {str(e)}", 500)
