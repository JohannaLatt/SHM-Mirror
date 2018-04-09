import pika
from enum import Enum
import configparser
import queue


class MSG_FROM_MIRROR_KEYS(Enum):
    MIRROR_READY = 1
    MIRROR_TRACKING_STARTED = 2
    MIRROR_TRACKING_DATA = 3
    MIRROR_TRACKING_LOST = 4


class MSG_TO_MIRROR_KEYS(Enum):
    TEXT = 1


# Callback for consuming incoming messages
def consume_server_message(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


def init():
    # Save the queue
    global queue
    queue = queue.Queue()

    # Create a local messaging connection
    Config = configparser.ConfigParser()
    Config.read('./config/mirror_config.ini')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=Config.get('General', 'messaging_ip')))

    global __channel
    __channel = connection.channel()

    # Create an exchange for the mirror-messages - type is direct so we can distinguish the different messages
    __channel.exchange_declare(exchange='from-mirror', exchange_type='direct')
    __channel.exchange_declare(exchange='to-mirror', exchange_type='direct')

    # Declare a queue to be used (random name will be used)
    result = __channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    # Listen to server messages
    for msg_keys in MSG_TO_MIRROR_KEYS:
        __channel.queue_bind(exchange='to-mirror',
                           queue=queue_name,
                           routing_key=msg_keys.name)

    __channel.basic_consume(consume_server_message,
                          queue=queue_name,
                          no_ack=True)


def start_consuming():
    __channel.start_consuming()


def start_sending():
    while True:
        item = queue.get()
        if item is None:
            continue
        try:
            __channel.basic_publish(exchange='from-mirror',
                              routing_key=item['key'],
                              body=item['body'])
        except pika.exceptions.ConnectionClosed as cce:
            print('[error] %r' % cce)
        queue.task_done()


def send(key, body):
    if __channel is None:
        init()

    if key not in MSG_FROM_MIRROR_KEYS.__members__:
        print("[error] %r is not a valid message key to send to the server" % key)
    else:
        queue.put({'key': key, 'body': body})
