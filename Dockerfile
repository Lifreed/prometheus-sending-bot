FROM python:3.6-alpine

ENV LIBRARY_PATH=/lib:/usr/lib

ENV BOT_ENDPOINT=$BOT_ENDPOINT
ENV FIRST_BOT_TOKEN=$FIRST_BOT_TOKEN
ENV SECOND_BOT_TOKEN=$SECOND_BOT_TOKEN

VOLUME ["/tmp"]
WORKDIR "/tmp"

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev libffi-dev libressl-dev
RUN apk add --no-cache py-cryptography

RUN python3 -m pip install dialog_bot_sdk prometheus-client

COPY . /tmp

CMD ["python3", "/tmp/main.py"]
