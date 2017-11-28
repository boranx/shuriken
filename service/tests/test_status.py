import pytest
import json
from core import app, tasks, status
from mock import MagicMock

def test_task_status_success():
    status.TaskStatus.get = MagicMock(return_value="{ \"Status\": \"SUCCESS\", \"description\": \"Task run successfully\"}")
    call = status.TaskStatus.get(3213123213)
    state = json.loads(call.decode('utf8'))['Status']
    result = json.loads(call.decode('utf8'))['description']
    assert state == "SUCCESS"
    assert result == "Task run successfully"
