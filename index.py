import threading

import messaging as Messaging
import rendering as Rendering


Messaging.init(Rendering)

thread_incoming_msgs = threading.Thread(target=Messaging.start_consuming)
thread_incoming_msgs.daemon = True
thread_incoming_msgs.start()

thread_outgoing_msgs = threading.Thread(target=Messaging.start_sending)
thread_outgoing_msgs.daemon = True
thread_outgoing_msgs.start()

Rendering.init_gui(Messaging)
