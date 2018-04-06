from flask import Flask
import pika
import socket
from enum import Enum

app = Flask(__name__)



# Create a local messaging connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create an exchange for the mirror-messages - just send out all messages to all consumers
channel.exchange_declare(exchange='mirror', exchange_type='direct')


class MIRROR_KEY(Enum):
    MIRROR_READY = 1
    MIRROR_TRACKING_STARTED = 2
    MIRROR_TRACKING_DATA = 3
    MIRROR_TRACKING_LOST = 4


@app.route("/")
def hello():
    channel.basic_publish(exchange='mirror',
                        routing_key=MIRROR_KEY.MIRROR_READY.name,
                        body='')
    return "Hello World!"


@app.route("/tracking")
def tracking():
    channel.basic_publish(exchange='mirror',
                      routing_key=MIRROR_KEY.MIRROR_TRACKING_DATA.name,
                      body='2 21 123 23 1231 346 6340 0304 23 2')
    return "It is tracking something"


app.run(host='0.0.0.0', port=5000, debug=False)
