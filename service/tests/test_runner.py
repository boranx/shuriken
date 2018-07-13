import json
import pytest
from core import app
import time

TEST_RESULT_ID = ''


@pytest.fixture
def client(request):
    test_client = app.test_client()

    def teardown():
        pass  # databases and resourses have to be freed at the end. But so far we don't have anything

    request.addfinalizer(teardown)
    return test_client


def post_json(client, url, json_dict):
    """Send dictionary json_dict as a json to the specified url """
    return client.post(url, data=json.dumps(json_dict), content_type='application/json')


def json_of_response(response):
    """Decode json from response"""
    return json.loads(response.data.decode('utf8'))


def test_healthcheck(client):
    response = client.get('/healthcheck')
    assert b'healthy' in response.data


def test_command_run_successfully(client):
    response = post_json(client, '/command/execute', {
        "command": "ls"
    })
    assert response.status_code == 200
    result_set = json_of_response(response)
    global TEST_RESULT_ID
    TEST_RESULT_ID = result_set['task_id']
    URL = "/command/status/{}".format(TEST_RESULT_ID)
    time.sleep(1)  # in order to assigning a worker time.
    loop = True
    while loop:
        response = client.get(URL)
        result = json_of_response(response)['Status']
        if result != "SUCCESS":
            loop = True
            print("Initialization")
            time.sleep(1)
        else:
            loop = False


def test_status_finished(client):
    URL = "/command/status/{}".format(TEST_RESULT_ID)
    response = client.get(URL)
    result = json_of_response(response)['Status']
    assert result == "SUCCESS"
    assert response.status_code == 200


def test_status_not_exist(client):
    response = client.get('/command/status/notfoundtaskid')
    assert b'Task is waiting for execution or unknown' in response.data
    assert response.status_code == 420


def test_status_exist(client):
    URL = "/command/status/{}".format(TEST_RESULT_ID)
    response = client.get(URL)
    assert response.status_code == 200


def test_output_not_exist(client):
    response = client.get('/command/output/notfoundtaskid')
    assert b'Task is waiting for execution or unknown' in response.data
    assert response.status_code == 420


def test_output_exist(client):
    URL = "/command/output/{}".format(TEST_RESULT_ID)
    response = client.get(URL)
    assert response.status_code == 200


def test_description_for_finished_task(client):
    URL = "/command/status/{}".format(TEST_RESULT_ID)
    response = client.get(URL)
    result = json_of_response(response)['description']
    assert result == "Task run successfully"
