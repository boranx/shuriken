FROM ubuntu:16.04
RUN apt-get update && apt-get install -y \
	python \
	python-pip \
	make

ADD . ./app
WORKDIR /app
RUN pip install --upgrade pip && \
	pip install -r service/requirements.txt

EXPOSE 5672
ENTRYPOINT [ "make", "worker" ]
