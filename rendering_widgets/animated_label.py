from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock

from functools import partial


class AnimatedLabel(Label):

    def __init__(self, **kwargs):
        super(AnimatedLabel, self).__init__(**kwargs)
        self.size_hint = (0, 0)
        self.color = (1, 1, 1)
        self.opacity = 0
        self.font_size = 40
        self.bold = True
        self.text_id = None

    def set_pos(self, x, y):
        self.pos = (x, y)

    # Set position in percentage of the screen (x = left, y = bottom)
    def set_pos_hint(self, x, y):
        self.pos_hint = {"x": x, "y": y}

    def set_text(self, text):
        self.text = text

    def set_id(self, id):
        self.text_id = id

    def get_id(self):
        return self.text_id

    def show(self):
        self.opacity = 1

    def hide(self):
        self.opacity = 0

    def fade_in(self, time=1, start=True):
        self.cancel_animations()

        self.anim_in = Animation(opacity=1.0, duration=time)
        if start:
            self.anim_in.start(self)
        return self.anim_in

    def fade_out(self, time=1, start=True, cb=lambda x, y: True):
        self.cancel_animations()

        self.anim_out = Animation(opacity=0.0, duration=time)
        self.anim_out.bind(on_complete=cb)
        if start:
            self.anim_out.start(self)
        return self.anim_out

    # Callback does nothing on default
    def fade_in_and_out(self, time_in=2, stay=5, time_out=2, cb=lambda x, y: True):
        self.cancel_animations()

        self.anim_in = self.fade_in(time_in, False)

        def fade_out_and_notify(time, cb, *largs):
            self.anim_out = self.fade_out(time, False)
            self.anim_out.bind(on_complete=cb)
            self.anim_out.start(self)

        self.anim_in.bind(on_complete=Clock.schedule_once(partial(fade_out_and_notify, time_out, cb), stay))
        self.anim_in.start(self)

    def cancel_animations(self):
        Animation.cancel_all(self)

    def get_left_x(self):
        return self.center_x - self.texture_size[0] * 0.5

    def get_bottom_y(self):
        return self.center_y + self.texture_size[1] * 0.5