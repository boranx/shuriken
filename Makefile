# It's necessary to set this because some environments don't link sh -> bash.
SHELL := /bin/bash

# We don't need make's built-in rules.
MAKEFLAGS += --no-builtin-rules
.SUFFIXES:

test:
	@docker-compose -f tool/docker-compose.yml rm -f && docker-compose -f tool/docker-compose.yml up -d
	@until curl localhost:5672; do echo "Waiting for amqp"; sleep 2; done
	@pushd service && celery -A core.celery worker --loglevel=info --detach && sleep 3 && pytest -vvv && popd
	@pkill -9 -f 'celery worker'
ci:
	@echo "Running Celery worker"
	@pushd service && celery -A core.celery worker --loglevel=info --detach && sleep 5 && pytest -vvv && popd

clean:
	@echo "Cleaning ..."
	@rm -rf	./service/core/*.pyc ./service/*.pyc ./service/tests/*.pyc ./service/.cache ./service/tests/__pycache__ ./service/celeryd.pid

worker:
	@echo "Starting Worker process"
	@cd service && celery -A core.celery worker --loglevel=info # ( --detach )

queue:
	@docker-compose -f tool/docker-compose.yml up -d

service:
	@echo "Starting Service"
	@cd service && python run_server.py

.DEFAULT_GOAL := test
.PHONY: test clean service worker ci
