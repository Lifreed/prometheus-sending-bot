from core import SDK
from dialog_api import messaging_pb2, sequence_and_updates_pb2
from prometheus_client import start_http_server, Gauge
import time
import datetime as dt
import os
import random
from google.protobuf import empty_pb2
from threading import Thread


REQUEST_TIME = Gauge('message_send_receive_seconds', 'Time spent processing request')
received = False


def send(peer, message):
    msg = messaging_pb2.MessageContent()
    msg.textMessage.text = message

    bot1.messaging.SendMessage(
        messaging_pb2.RequestSendMessage(
            peer=peer,
            deduplication_id=random.randint(0, 100000000),
            message=msg
            )
        )

    print('message sent ' + str(dt.datetime.now()) + ':', message)


def gen_random_message(length=20):
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '
    result = ''
    for _ in range(length):
        result += alphabet[random.randint(0, len(alphabet)-1)]

    return result


def seq_handler():
    global received
    for update in bot2.updates.SeqUpdates(empty_pb2.Empty()):
        up = sequence_and_updates_pb2.UpdateSeqUpdate()
        up.ParseFromString(update.update.value)
        if up.updateMessage.message.textMessage.text == message_text:
            received = True
            break


if __name__ == '__main__':
    bot1 = SDK(os.environ.get('BOT_ENDPOINT'))
    bot2 = SDK(os.environ.get('BOT_ENDPOINT'))

    token1 = os.environ.get('FIRST_BOT_TOKEN')
    token2 = os.environ.get('SECOND_BOT_TOKEN')

    start_http_server(8080)

    counter = 0
    while True:
        try:
            print('counter =', counter, dt.datetime.now())
            counter += 1
            received = False
            message_text = gen_random_message()

            bot1_user_info = bot1.bot_authorize(token1)
            bot2_user_info = bot2.bot_authorize(token2)

            bot2_outpeer = bot1.find_user_outpeer_by_nick(bot2_user_info.user.data.nick.value)

            bot2_thread = Thread(target=seq_handler).start()

            start_time = time.time()
            send(bot2_outpeer, message_text)

            while True:
                if time.time() - start_time >= 10:
                    REQUEST_TIME.set(1000)
                    break
                if received:
                    print('message received ' + str(dt.datetime.now()) + ':', message_text)
                    REQUEST_TIME.set(time.time() - start_time)
                    break

            bot1.logout()
            bot2.logout()
            time.sleep(1)
        except Exception as e:
            print(e)
            continue
