from utils.enums import MSG_FROM_MIRROR_KEYS
from utils.enums import MSG_TO_MIRROR_KEYS

from amqpstorm import Connection

import configparser
import queue


# Callback for consuming incoming messages
def consume_server_message(message):
    # print("[Messaging][info] Received {}:{}...".format(message.method['routing_key'], message.body[0:80]))
    rendering.render(message.method['routing_key'], message.body)


def init(Rendering):
    global rendering
    rendering = Rendering

    # Save the queue
    global queue
    queue = queue.Queue()

    # Create a local messaging connection
    Config = configparser.ConfigParser()
    Config.read('./config/mirror_config.ini')
    connection = Connection(Config.get('General', 'messaging_ip'), 'guest', 'guest')

    global __channel
    __channel = connection.channel()

    # Create an exchange for the mirror-messages - type is direct so we can distinguish the different messages
    __channel.exchange.declare(exchange='from-mirror', exchange_type='direct')
    __channel.exchange.declare(exchange='to-mirror', exchange_type='direct')

    # Declare a queue to be used (random name will be used)
    result = __channel.queue.declare(exclusive=True)
    queue_name = result['queue']

    # Listen to server messages
    for msg_keys in MSG_TO_MIRROR_KEYS:
        __channel.queue.bind(exchange='to-mirror',
                           queue=queue_name,
                           routing_key=msg_keys.name)

    __channel.basic.consume(consume_server_message,
                          queue=queue_name,
                          no_ack=True)


def start_consuming():
    __channel.start_consuming()


# Threadsafe sending of messages
def start_sending():
    while True:
        item = queue.get()
        if item is None:
            continue
        __channel.basic.publish(exchange='from-mirror',
                          routing_key=item['key'],
                          body=item['body'])
        print("[Messaging][info] Sent {}: {}".format(item['key'], item['body'][0:50]))
        queue.task_done()


def send(key, body):
    if __channel is None:
        init()

    if key not in MSG_FROM_MIRROR_KEYS.__members__:
        print("[Messaging][error] %r is not a valid message key to send to the server" % key)
    else:
        queue.put({'key': key, 'body': body})
