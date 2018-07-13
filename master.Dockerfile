FROM python:3.6.4
RUN apt-get update && apt-get install -y \
	make

ADD . ./app
WORKDIR /app
RUN pip3.6 install --upgrade pip==9.0.3 && \
	pip3.6 install -r service/requirements.txt

EXPOSE 5000 5672
ENTRYPOINT [ "make", "service" ]
