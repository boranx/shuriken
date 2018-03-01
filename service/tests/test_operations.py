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


def test_node_is_activated(client):
    response = client.get('/node/active')
    assert b'celery@' in response.data
    assert response.status_code == 200
