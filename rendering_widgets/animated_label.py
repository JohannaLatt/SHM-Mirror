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

    def set_pos(self, x, y):
        self.pos = (x, y)

    # Set position in percentage of the screen (x = left, y = bottom)
    def set_pos_hint(self, x, y):
        self.pos_hint = {"x": x, "y": y}

    def set_text(self, text):
        self.text = text

    def fade_in(self, time=1, start=True):
        anim = Animation(opacity=1.0, duration=time)
        if start: anim.start(self)
        return anim

    def fade_out(self, time=1, start=True):
        anim = Animation(opacity=0.0, duration=time)
        if start: anim.start(self)
        return anim

    def fade_in_and_out(self, time_in=2, stay=5, time_out=2, cb=lambda x, y: True):
        anim_in = self.fade_in(time_in, False)

        def fade_out_and_notify(time, cb, *largs):
            anim_out = self.fade_out(time, False)
            anim_out.bind(on_complete=cb)
            anim_out.start(self)

        anim_in.bind(on_complete=Clock.schedule_once(partial(fade_out_and_notify, time_out, cb), stay))
        anim_in.start(self)

    def get_left_x(self):
        return self.center_x - self.texture_size[0] * 0.5

    def get_bottom_y(self):
        return self.center_y + self.texture_size[1] * 0.5
