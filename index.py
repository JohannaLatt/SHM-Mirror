from flask import Flask
import _thread
import messaging as Messaging
from messaging import MSG_FROM_MIRROR_KEYS


app = Flask(__name__)

Messaging.init()
_thread.start_new_thread(Messaging.start_consuming, ())


@app.route("/")
def hello():
    Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_READY.name, "")
    return "Hello World!"


@app.route("/tracking")
def tracking():
    Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_TRACKING_DATA.name, "2 34 23 194 93834 1828 02")
    return "It is tracking something"

app.run(host='0.0.0.0', port=5000, debug=False)
