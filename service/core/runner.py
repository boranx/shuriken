from core import tasks, app
from flask import Flask, request, jsonify, abort

@app.route("/command/execute", methods=['POST'])
def command_runner():
    try:
        content = request.json
        cmd = content['command']
    except Exception, e:
        return jsonify(missing_parameter_error=repr(e)), 404

    task_result = tasks.cmd_runner.apply_async([cmd], queue='default')
    return jsonify(task_id=task_result.id), 200

@app.route("/command/broadcast", methods=['POST'])
def broadcast():
    try:
        content = request.json
        cmd = content['command']
    except Exception, e:
        return jsonify(missing_parameter_error=repr(e)), 404

    task_result = tasks.cmd_runner.apply_async([cmd], queue='broadcast_tasks')
    return jsonify(task_id=task_result.id), 200

@app.route("/healthcheck", methods=['GET'])
def healthcheck():
    return jsonify(status="healthy"), 200
