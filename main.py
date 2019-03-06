from dialog_bot_sdk.bot import DialogBot
import grpc
from prometheus_client import start_http_server, Gauge
import time
import os
import random

REQUEST_TIME = Gauge('message_send_receive_seconds', 'Time spent processing request')
received = False


@REQUEST_TIME.time()
def send(peer, message):
    global received
    bot1.messaging.send_message(peer, message)
    print('message sent:', message)
    while True:
        if received:
            break


def on_msg_bot2(*params):
    global received
    if params[0].message.textMessage.text == message_text:
        print('message received:', params[0].message.textMessage.text)
        received = True


def gen_random_message(length=20):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
    result = ''
    for _ in range(length):
        result += alphabet[random.randint(0, len(alphabet)-1)]

    return result


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

    bot2_peer = bot1.users.find_user_outpeer_by_nick(bot2.user_info.user.data.nick.value)
    bot2.messaging.on_message_async(on_msg_bot2)

    start_http_server(8080)

    while True:
        received = False
        message_text = gen_random_message()
        send(bot2_peer, message_text)
        time.sleep(1)
