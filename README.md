# Shuriken

Shuriken is a distributed compute engine that horizontally scalable. It uses RabbitMQ as task queue, execute your commands on the workers.

## Requirements

* Vagrant - 1.x.x or 2.x.x

## Run

```shell
vagrant ssh
cd /vagrant # After that, you are ready to go.
make queue # Run a Rabbitmq if you don't have. You can edit endpoints in config file if you have.
make service # Run this in one terminal
make service # Run this in another terminal. You can execute multiple times on one node or on different nodes.
```

## Example Requests

API Default port : 5000

POST /command/execute
Payload :

```json
{
    "command":"ls"
}
```

And the response should be like :

```json
{
    "task_id": "45e972c3-5227-4982-bed9-f475d925825e"
}
```

GET /command/status/45e972c3-5227-4982-bed9-f475d925825e

And the response should be like :

```json
{
    "Status": "SUCCESS",
    "description": "Task run successfully"
}
```

GET /command/output/45e972c3-5227-4982-bed9-f475d925825e

And the response should be like : (This is not json btw)

celeryd.pid
config.ini
core
requirements.txt
run_server.py
tests

And you can request the status of a task. The workers will take the task and then execute.

## Development

```shell
vagrant up # Which will create a VM using Virtualbox, imports current folder as shared folder, install the dependencies from scratch.
vagrant ssh
cd /vagrant # After that, you are ready to go.
make ...
```

## Tests

```shell
make test
```
