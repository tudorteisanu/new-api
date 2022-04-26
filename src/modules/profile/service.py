from flask import request
from flask import jsonify


class ProfileService:
    def show(self):
        resp = {
            "message": 2
        }

        return jsonify(resp)

    def update(self):
        data = request.json
        return jsonify(data)

