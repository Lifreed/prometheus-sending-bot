FROM python:3.7

ENV LIBRARY_PATH=/lib:/usr/lib

ENV BOT_ENDPOINT=$BOT_ENDPOINT
ENV FIRST_BOT_TOKEN=$FIRST_BOT_TOKEN
ENV SECOND_BOT_TOKEN=$SECOND_BOT_TOKEN

WORKDIR "/tmp"

COPY . /tmp

RUN python3 -m pip install -r requirements.txt

EXPOSE 8080

CMD ["python3", "/tmp/main.py"]
