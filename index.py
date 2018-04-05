from flask import Flask
import pika
import socket

app = Flask(__name__)



# Create a local messaging connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create an exchange for the mirror-messages - just send out all messages to all consumers
channel.exchange_declare(exchange='mirror', exchange_type='direct')


@app.route("/")
def hello():
    channel.basic_publish(exchange='mirror',
                        routing_key='mirror-ready',
                        body='')
    return "Hello World!"


@app.route("/Tracking")
def tracking():
    channel.basic_publish(exchange='mirror',
                      routing_key='mirror-tracking',
                      body='2 21 123 23 1231 346 6340 0304 23 2')
    return "It is tracking something"
