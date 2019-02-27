# Bot for testing message sending with export metrics to Prometheus

## Build
```bash
docker build -t message-test-bot .
```

## Run 
```bash
docker run -t -p 8080:8080 message-test-bot
```

## Environment variables

Set them in Dockerfile:

`BOT_ENDPOINT` - endpoint for watching

`FIRST_BOT_TOKEN` - token for first bot

`SECOND_BOT_TOKEN` - token for second bot

