test:
	@docker-compose -f tool/docker-compose.yml rm -f && docker-compose -f tool/docker-compose.yml up -d
	@cd service && celery -A core.celery worker --loglevel=info --detach
	@cd service && pytest -vvv
	@pkill -9 -f 'celery worker'

ci:
	@echo "Running Celery worker"
	@cd service && celery -A core.celery worker --loglevel=info --detach
	@sleep 5
	@cd service && pytest -vvv

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
.PHONY: test clean service worker
