from utils.enums import MSG_TO_MIRROR_KEYS, MSG_FROM_MIRROR_KEYS
from rendering_widgets.gui_base import GUIBase


import json


def init_gui(Messaging):
    print('[Rendering][info] Initializing GUI')
    # import rendering_widgets.gui_base as GUIBase

    global gui
    gui = GUIBase()
    Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_READY.name, '')
    gui.run()


# Called by kivy
def render(view, data):
    try:
        gui
    except NameError:
        print('[Rendering][warning] Message discarded, rendering not initialized yet')
    else:
        if view == MSG_TO_MIRROR_KEYS.TEXT.name:
            data = decode_data(data)
            gui.show_text(data)
        elif view == MSG_TO_MIRROR_KEYS.CLEAR_SKELETON.name:
            gui.clear_skeleton()
        elif view == MSG_TO_MIRROR_KEYS.RENDER_SKELETON.name:
            data = decode_data(data)
            gui.render_skeleton_data(data)
        elif view == MSG_TO_MIRROR_KEYS.CHANGE_SKELETON_COLOR.name:
            data = decode_data(data)
            gui.change_joint_or_bone_color(data)
        elif view == MSG_TO_MIRROR_KEYS.UPDATE_GRAPHS.name:
            data = decode_data(data)
            gui.update_graps(data)
        else:
            print('[Rendering][warning] %r is not a suported view' % view)

def decode_data(data):
    try:
        data = json.loads(data)
    except json.decoder.JSONDecodeError:
        print('[Rendering][warning] Message discarded, could not decode json: {}'.format(data))
    else:
        return data
