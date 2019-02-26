from dialog_bot_sdk.bot import DialogBot
import grpc
from prometheus_client import start_http_server, Gauge
import time
import os


REQUEST_TIME = Gauge('message_send_receive_seconds', 'Time spent processing request')


@REQUEST_TIME.time()
def send():
    bot1.messaging.send_message(peer, 'Test')


if __name__ == '__main__':
    bot1 = DialogBot.get_secure_bot(
        os.environ.get('BOT_ENDPOINT'),  # grpc-test.transmit.im:9443
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        os.environ.get('FIRST_BOT_TOKEN')  # b7cc677c0eee2743c496b8f949a14a82a83be8c9
    )

    bot2 = DialogBot.get_secure_bot(
        os.environ.get('BOT_ENDPOINT'),  # grpc-test.transmit.im:9443
        grpc.ssl_channel_credentials(),  # SSL credentials (empty by default!)
        os.environ.get('SECOND_BOT_TOKEN')  # 95f65e69776b5ac23931e11794b0ed4c17147c61
    )

    peer = bot1.users.find_user_outpeer_by_nick(os.environ.get('SECOND_BOT_NICKNAME'))

    start_http_server(8000)

    while True:
        send()
        time.sleep(1)
