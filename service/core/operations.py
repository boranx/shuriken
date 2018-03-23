from core import tasks, app
from flask import Flask, request, jsonify, abort, redirect, url_for
from core import celery


@app.route("/")
def root():
    """Route to Swagger
    This is using docstrings for specifications.
    ---
    tags:
    - Operations & Management
        """
    return redirect(url_for('flasgger.apidocs'))


@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    """API Healthcheck
    This is using docstrings for specifications.
    ---
    tags:
    - Operations & Management
    responses:
        200:
            description: Number of active nodes
            schema:
                $ref: '#/healthcheck'
            examples:
                {
                    "status": "healthy"
                }
        """
    return jsonify(status="healthy"), 200


@app.route("/node/active", methods=['GET'])
def node_count():
    """Show active nodes and counts
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
