import pytest
from mock import patch
from core.tasks import cmd_runner

class Test_celery_tasks:
    @patch('core.tasks.cmd_runner.apply_async')
    def test_task_id_returns(self, calling):
        cmd = ""
        result = cmd_runner.apply_async([cmd])
        meta = calling.assert_called_with([cmd])
        assert result.id is not None

    # @patch('core.tasks.cmd_runner.apply_async.Popen')
    # def test_task_create_process(self, mock):
    #     cmd = "echo 'test'"
    #     mock.return_value = "{'description': 'Task run successfully', 'output': 'test\n', 'returncode': 0}"
    #     result = cmd_runner.apply([cmd]).get()
    #     assert result == mock.called
