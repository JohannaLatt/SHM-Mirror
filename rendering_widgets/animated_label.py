from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window

from functools import partial


class AnimatedLabel(Label):
    def __init__(self, **kwargs):
        kwargs["font_size"] = kwargs["font_size"] * (((Window.width / 1700) + 0.2) + ((Window.height / 900) * .1))

        super().__init__(**kwargs)

        if kwargs["size_hint"] == (1, 1):  # Static text --> make it fullscreen so we can use halign
            self.bind(texture_size=self.setter('size'))
            self.text_size = Window.size[0], 0

        self.opacity = 0
        self.bold = True
        self.text_id = None

        self.clock_event = None
        self.anim_in = None
        self.anim_out = None

    def set_pos(self, x, y):
        self.pos = (x, y)

    # Set position in percentage of the screen (x = left, y = bottom)
    def set_pos_hint(self, hint):
        self.pos_hint = hint

    def set_text(self, text):
        self.text = text

    def set_color(self, color):
        self.color = color

    def set_id(self, id):
        self.text_id = id

    def get_id(self):
        return self.text_id

    def set_font_size(self, size):
        self.font_size = size

    def show(self):
        self.opacity = 1

    def hide(self):
        self.opacity = 0

    def fade_in(self, time=1, start=True):
        if self.anim_in is not None:
            self.anim_in.cancel(self)

        self.anim_in = Animation(opacity=1.0, duration=time)
        if start:
            self.anim_in.start(self)
        return self.anim_in

    def fade_out(self, time=1, start=True, cb=lambda x, y: True):
        if self.anim_out is not None:
            self.anim_out.cancel(self)

        self.anim_out = Animation(opacity=0.0, duration=time)
        self.anim_out.bind(on_complete=cb)
        if start:
            self.anim_out.start(self)
        return self.anim_out

    # Callback does nothing on default
    def fade_in_and_out(self,
                        time_in=2,
                        stay=5,
                        time_out=2,
                        cb=lambda x, y: True):
        self.cancel_animations()

        self.anim_in = self.fade_in(time_in, False)

        def fade_out_and_notify(time, cb, *largs):
            self.anim_out = self.fade_out(time, False)
            self.anim_out.bind(on_complete=cb)
            self.anim_out.start(self)

        self.clock_event = Clock.schedule_once(
            partial(fade_out_and_notify, time_out, cb), stay)
        self.anim_in.bind(on_complete=self.clock_event)
        self.anim_in.start(self)

    def cancel_animations(self):
        Animation.cancel_all(self)
        if self.clock_event is not None:
            self.clock_event.cancel()

    def get_left_x(self):
        return self.center_x - self.texture_size[0] * 0.5

    def get_bottom_y(self):
        return self.center_y + self.texture_size[1] * 0.5
