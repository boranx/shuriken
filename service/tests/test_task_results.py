from pytest import raises
from celery.exceptions import Retry
from mock import patch
import unittest

from core.tasks import cmd_runner

class Test_celery_task_results:
    def test_command_result(self):
        rst = cmd_runner.apply(["echo 'test' && /bin/true"]).get()
        assert 'test' in str(rst)
        assert 'Task run successfully' in str(rst)
        assert '\'returncode\': 0' in str(rst)

    def test_command_execution(self):
        rst = cmd_runner.apply(["ls"]).get()
        assert 'config.ini' in str(rst)
        assert 'Task run successfully' in str(rst)
        assert '\'returncode\': 0' in str(rst)

    def test_hostname_returns_successfully(self):
        rst = cmd_runner.apply(["echo 'foo' && /bin/true"]).get()
        assert 'foo' in str(rst)
        assert 'Task run successfully' in str(rst)
        assert 'hostname' in str(rst)
        assert '\'returncode\': 0' in str(rst)
