from flask_restful import Resource, Api
from core import api, celery, app
import tasks


class TaskStatus(Resource):
    def get(self, task_id):
        task = tasks.cmd_runner.AsyncResult(task_id)
        if task.state == 'PENDING':
            result = "Task not found"
            resp = app.make_response((result, 404))
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
