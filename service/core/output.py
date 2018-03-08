from flask_restful import Resource, Api
from flask import jsonify
from core import api, celery, app
import tasks, json


class TaskOutput(Resource):
    def get(self, task_id):
        """Show a Task Output
        ---
        tags:
        - Tasks
        parameters:
            - in: path
              name: task_id
              type: string
              required: true
              description: The uuid of your task.
        responses:
            200:
                description: Show a Task Output
                schema:
                    $ref: '#/command/output/<TaskId>'
                examples:
                    {
                        "output": "foo\n",
                        "hostname": "celery@vagrant",
                        "returncode": 0,
                        "description": "Task run successfully"
                    }
            """
        task = tasks.cmd_runner.AsyncResult(task_id)
        if task.state == 'PENDING':
            result = "Task is waiting for execution or unknown"
            resp = app.make_response((jsonify(status=result), 420))
            return resp
        result = task.info
        jsonResult = json.dumps(result, ensure_ascii=False)
        resp = app.make_response((jsonResult, 200))
        resp.headers['content-type'] = 'text/plain'
        return resp


api.add_resource(TaskOutput, '/command/output/<string:task_id>')
