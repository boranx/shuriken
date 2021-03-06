from core import  app
from flask import Flask, request, jsonify, abort
import core.tasks as executor


@app.route("/command/execute", methods=['POST'])
def command_runner():
    """
    Single Execution
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        description: The full body.
        schema:
          required:
            - command
          properties:
            command:
              type: string
              description: The command's name.
              default: "echo 'foo'"
    responses:
      200:
        description: OK
        schema:
          $ref: '#/command/execute'
        examples:
            {
                "task_id": "45e972c3-5227-4982-bed9-f475d925825e"
            }
    """
    try:
        content = request.json
        cmd = content['command']
    except Exception as e:
        return jsonify(missing_parameter_error=repr(e)), 404

    task_result = executor.cmd_runner.apply_async([cmd], queue='default')
    return jsonify(task_id=task_result.id), 200


@app.route("/command/broadcast", methods=['POST'])
def broadcast():
    """
    Broadcast Execution
    ---
    tags:
      - Tasks
    parameters:
      - name: body
        in: body
        required: true
        description: The full body.
        schema:
          required:
            - command
          properties:
            command:
              type: string
              description: The command's name that will be broadcasted.
              default: "sudo apt-get update"
    responses:
      200:
        description: OK
        schema:
          $ref: '#/command/broadcast'
        examples:
            {
                "task_id": "45e972c3-5227-4982-bed9-f475d925825e"
            }
    """
    try:
        content = request.json
        cmd = content['command']
    except Exception as e:
        return jsonify(missing_parameter_error=repr(e)), 404

    task_result = executor.cmd_runner.apply_async([cmd], queue='broadcast')
    return jsonify(task_id=task_result.id), 200
