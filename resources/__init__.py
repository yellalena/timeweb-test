from flask import make_response, jsonify
from flask_restful import Resource


def resp(tag, msg, statusno):
    return make_response(jsonify({tag: msg}), statusno)


def err(msg, errno):
    return resp('err', msg, errno)


class Ping(Resource):
    def post(self):
        return resp("ping",
                    "hello",
                    200)