from flask_restful import Resource, Api
from flask import jsonify
from core import api, celery, app
import tasks


class TaskStatus(Resource):
    def get(self, task_id):
        """Show a Task Status
        This is using docstrings for specifications.
        ---
        responses:
            200:
                description: Show a Task Status
                schema:
                    $ref: '#/command/status/<TaskId>'
                examples:
                    {
                        "Status": "SUCCESS",
                        "description": "Task run successfully"
                    }
            """
        task = tasks.cmd_runner.AsyncResult(task_id)
        if task.state == 'PENDING':
            result = "Task is waiting for execution or unknown"
            resp = app.make_response((jsonify(status=result), 420))
            return resp
        elif task.state == 'PROGRESS':
            result_obj = {'Status': "PROGRESS",
                          'description': "Task is currently running",
                          'returncode': None}
        else:
            try:
                return_code = task.info['returncode']
                description = task.info['description']
                if return_code is 0:
                    result_obj = {'Status': "SUCCESS",
                                  'description': description}
                else:
                    result_obj = {'Status': "TASK_FAILURE",
                                  'description': description,
                                  'returncode': return_code}
            except:
                result_obj = {'Status': "CELERY_FAILURE"}

        return result_obj


api.add_resource(TaskStatus, '/command/status/<string:task_id>')
