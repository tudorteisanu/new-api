from flask import request, jsonify

from src.app import app, FlaskConfig
from celery_app import create_task


@app.route("/tasks", methods=["GET"])
def run_task():
    task = create_task.delay(int(5))
    return jsonify({"task_id": task.id}), 202


if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
