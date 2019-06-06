FROM python:3.7

ENV LIBRARY_PATH=/lib:/usr/lib

ENV BOT_ENDPOINT=$BOT_ENDPOINT
ENV FIRST_BOT_TOKEN=$FIRST_BOT_TOKEN
ENV SECOND_BOT_TOKEN=$SECOND_BOT_TOKEN

WORKDIR "/tmp"

RUN python3 -m pip install dialog_bot_sdk==2.1.1 prometheus-client

COPY . /tmp

CMD ["python3", "/tmp/main.py"]
