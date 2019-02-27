# Bot for testing message sending with export metrics to Prometheus

ATTENTION! It starts local server and sends metrics to 8000 port.

## Build
```bash
docker build -t message-test-bot .
```

## Run 
```bash
docker run -p 8000:8000 message-test-bot
```

## Environment variables

Set them in Dockerfile:

`BOT_ENDPOINT` - endpoint for watching

`FIRST_BOT_TOKEN` - token for first bot

`SECOND_BOT_TOKEN` - token for second bot

