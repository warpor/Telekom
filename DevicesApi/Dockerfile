FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /code/

RUN apt-get update \
    && apt-get install gcc default-libmysqlclient-dev -y

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
	

COPY . .

RUN chmod +x ./docker-entrypoint.sh

RUN apt-get install netcat -y
ENTRYPOINT ["bash", "/code/docker-entrypoint.sh"]
