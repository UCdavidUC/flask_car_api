FROM python:3.8-alpine

RUN apt update -y && \
    apt install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT["python3"]

CMD["api.py"]
