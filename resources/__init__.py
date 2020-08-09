import logging

from flask import make_response, jsonify
from flask_restful import Resource

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def resp(tag, msg, statusno):
    return make_response(jsonify({tag: msg}), statusno)


def err(msg, errno):
    return resp('err', msg, errno)


class Ping(Resource):
    def post(self):
        logger.info("Accepted a new request to ping")
        return resp("ping",
                    "hello",
                    200)