from flask import Response, jsonify, make_response
# from tensorboard import errors


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))
