FROM python:3.6-alpine

ENV LIBRARY_PATH=/lib:/usr/lib

ENV BOT_ENDPOINT=eem.dlg.im:443
ENV FIRST_BOT_TOKEN=263f0fd4a834decd86e5b082f603998bbd36821c
ENV SECOND_BOT_TOKEN=f9751379fbad3311ff4bc38e737af5330150e275

VOLUME ["/tmp"]
WORKDIR "/tmp"

RUN apk add build-base python-dev py-pip jpeg-dev zlib-dev libffi-dev libressl-dev
RUN apk add --no-cache py-cryptography

RUN python3 -m pip install dialog_bot_sdk prometheus-client

COPY . /tmp

CMD ["python3", "/tmp/main.py"]