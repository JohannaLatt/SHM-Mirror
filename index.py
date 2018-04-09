import _thread
import messaging as Messaging
import rendering as Rendering
import queue

queue = queue.Queue()

Messaging.init(queue)
_thread.start_new_thread(Messaging.start_consuming, ())
_thread.start_new_thread(Messaging.start_sending, (queue,))

Rendering.init_gui()
