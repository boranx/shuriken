from flask_restful import Resource, Api
from flask import jsonify
from core import api, celery, app
import tasks


class TaskOutput(Resource):
    def get(self, task_id):
        task = tasks.cmd_runner.AsyncResult(task_id)
        if task.state == 'PENDING':
            result = "Task is waiting for execution or unknown"
            resp = app.make_response((jsonify(status=result), 420))
            return resp
        if task.state == "PROGRESS":
            result = task.info['output']
        else:
            result = task.info['output']
        resp = app.make_response((result, 200))
        resp.headers['content-type'] = 'text/plain'
        return resp


api.add_resource(TaskOutput, '/command/output/<string:task_id>')
