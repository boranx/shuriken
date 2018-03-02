from core import tasks, app
from flask import Flask, request, jsonify, abort
from core import celery


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    return jsonify(status="healthy"), 200


@app.route("/node/active", methods=['GET'])
def node_count():
    """Show node active and counts
    This is using docstrings for specifications.
    ---
    tags:
    - Operations & Management
    responses:
        200:
            description: Number of active nodes
            schema:
                $ref: '#/node/active'
            examples:
                {
                    "celery@boran-UX305UA": [],
                    "celery@vagrant": []
                }
        """
    status = celery.control.inspect()
    if status.active() is not None:
        resp = app.make_response(jsonify(status.active()))
    else:
        result = "No active node found"
        resp = app.make_response((jsonify(status=result), 420))
    return resp
