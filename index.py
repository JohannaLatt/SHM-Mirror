import threading

import messaging as Messaging
import rendering as Rendering


Messaging.init(Rendering)

thread = threading.Thread(target=Messaging.start_consuming)
thread.daemon = True
thread.start()

thread = threading.Thread(target=Messaging.start_sending)
thread.daemon = True
thread.start()

Rendering.init_gui()
