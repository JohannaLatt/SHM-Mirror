import _thread
import messaging as Messaging
import rendering as Rendering


Messaging.init(Rendering)

_thread.start_new_thread(Messaging.start_consuming, ())
_thread.start_new_thread(Messaging.start_sending, ())

Rendering.init_gui()
