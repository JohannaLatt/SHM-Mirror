from utils.enums import MSG_TO_MIRROR_KEYS, MSG_FROM_MIRROR_KEYS
from rendering_widgets.health_mirror_gui import HealthMirrorGUI
from rendering_widgets.gui_base_kivy import GUIBase


from PyQt5 import QtWidgets

import json
import sys


def init_gui(Messaging):
    print('[Rendering][info] Initializing GUI')
    # import rendering_widgets.gui_base as GUIBase

    global gui
    gui = GUIBase()
    gui.run()

    '''app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Smart Health Mirror')

    global gui
    gui = HealthMirrorGUI(app)
    gui.show()

    print('[Rendering][info] GUI ready')
    Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_READY.name, '')

    sys.exit(app.exec_())'''


def render(view, data):
    try:
        gui
    except NameError:
        print('[Rendering][warning] Message discarded, rendering not initialized yet')
    else:
        if view == MSG_TO_MIRROR_KEYS.STATIC_TEXT.name:
            data = json.loads(data)
            #gui.show_static_text(data["text"], int(data["position"]))
        elif view == MSG_TO_MIRROR_KEYS.CLEAR_SKELETON.name:
            gui.clear_skeleton()
        elif view == MSG_TO_MIRROR_KEYS.RENDER_SKELETON.name:
            gui.render_skeleton_data(data)
        else:
            print('[Rendering][warning] %r is not a suported view' % view)
