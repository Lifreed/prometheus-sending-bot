FROM python:3.6-alpine

ENV LIBRARY_PATH=/lib:/usr/lib
ENV BOT_ENDPOINT=grpc-test.transmit.im:9443
ENV SECOND_BOT_NICKNAME=test_con_bot2
ENV FIRST_BOT_TOKEN=b7cc677c0eee2743c496b8f949a14a82a83be8c9
ENV SECOND_BOT_TOKEN=95f65e69776b5ac23931e11794b0ed4c17147c61

VOLUME ["/tmp"]
WORKDIR "/tmp"

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev libffi-dev libressl-dev
RUN apk add --no-cache py-cryptography

COPY ./requirements.txt /tmp/requirements.txt

RUN python3 -m pip install -r /tmp/requirements.txt

COPY . /tmp

CMD ["python3", "/tmp/main.py"]