from flask import Flask
import pika
import _thread
from enum import Enum

app = Flask(__name__)

class MSG_FROM_MIRROR_KEYS(Enum):
    MIRROR_READY = 1
    MIRROR_TRACKING_STARTED = 2
    MIRROR_TRACKING_DATA = 3
    MIRROR_TRACKING_LOST = 4


class MSG_TO_MIRROR_KEYS(Enum):
    TEXT = 1


# Create a local messaging connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create an exchange for the mirror-messages - type is direct so we can distinguish the different messages
channel.exchange_declare(exchange='from-mirror', exchange_type='direct')
channel.exchange_declare(exchange='to-mirror', exchange_type='direct')

# Declare a queue to be used (random name will be used)
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# Callback for consuming incoming messages
def consume_server_message(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

# Listen to server messages
for msg_keys in MSG_TO_MIRROR_KEYS:
    channel.queue_bind(exchange='to-mirror',
                       queue=queue_name,
                       routing_key=msg_keys.name)

channel.basic_consume(consume_server_message,
                      queue=queue_name,
                      no_ack=True)

_thread.start_new_thread(channel.start_consuming, ())


@app.route("/")
def hello():
    channel.basic_publish(exchange='from-mirror',
                        routing_key=MSG_FROM_MIRROR_KEYS.MIRROR_READY.name,
                        body='')
    return "Hello World!"


@app.route("/tracking")
def tracking():
    channel.basic_publish(exchange='from-mirror',
                      routing_key=MSG_FROM_MIRROR_KEYS.MIRROR_TRACKING_DATA.name,
                      body='2 21 123 23 1231 346 6340 0304 23 2')
    return "It is tracking something"


app.run(host='0.0.0.0', port=5000, debug=False)
