from utils.enums import MSG_TO_MIRROR_KEYS, MSG_FROM_MIRROR_KEYS
from rendering_widgets.gui_base_kivy import GUIBase


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
            data = json.loads(data)
            is_valid_data = check_text_arguments(data)

            if is_valid_data:
                gui.show_text(data)
        elif view == MSG_TO_MIRROR_KEYS.CLEAR_SKELETON.name:
            gui.clear_skeleton()
        elif view == MSG_TO_MIRROR_KEYS.RENDER_SKELETON.name:
            gui.render_skeleton_data(data)
        else:
            print('[Rendering][warning] %r is not a suported view' % view)


def check_text_arguments(data):
    if "text" not in data:
        return False

    if "position" not in data:
        data["position"] = (0.5, 0.9)
    if "id" not in data:
        data["id"] = None
    if "color" not in data:
        data["color"] = (1, 1, 1, 1)
    if "animation" not in data:
        data["animation"] = {}
        data["animation"]["fade_in"] = 2
        data["animation"]["stay"] = 5
        data["animation"]["fade_out"] = 2
    else:
        if "fade_in" not in data["animation"]:
            data["animation"]["fade_in"] = 2
        if "stay" not in data["animation"]:
            data["animation"]["stay"] = 5
        if "fade_out" not in data["animation"]:
            data["animation"]["fade_out"] = 2

    return True
