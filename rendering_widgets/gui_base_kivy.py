from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from random import random as r
from functools import partial


class GUIBase(App):

    def add_rects(self, label, wid, count, *largs):
        label.text = str(int(label.text) + count)
        with wid.canvas:
            for x in range(count):
                Color(r(), 1, 1, mode='hsv')
                Rectangle(pos=(r() * wid.width + wid.x,
                               r() * wid.height + wid.y), size=(20, 20))

    def double_rects(self, label, wid, *largs):
        count = int(label.text)
        self.add_rects(label, wid, count, *largs)

    def reset_rects(self, label, wid, *largs):
        label.text = '0'
        wid.canvas.clear()

    def build(self):
        wid = Widget()

        label = Label(text='0')

        btn_add100 = Button(text='+ 100 rects',
                            on_press=partial(self.add_rects, label, wid, 100))

        btn_add500 = Button(text='+ 500 rects',
                            on_press=partial(self.add_rects, label, wid, 500))

        btn_double = Button(text='x 2',
                            on_press=partial(self.double_rects, label, wid))

        btn_reset = Button(text='Reset',
                           on_press=partial(self.reset_rects, label, wid))

        layout = BoxLayout(size_hint=(1, None), height=50)
        layout.add_widget(btn_add100)
        layout.add_widget(btn_add500)
        layout.add_widget(btn_double)
        layout.add_widget(btn_reset)
        layout.add_widget(label)

        root = BoxLayout(orientation='vertical')
        root.add_widget(wid)
        root.add_widget(layout)

        return root


class MainCanvas(Widget):
    def __init__(self, **kwargs):
        super(MainCanvas, self).__init__(**kwargs)

        with self.canvas:
            # draw a line using the default color
            Line(points=(0, 100, 0, 100, 0, 100))

            # lets draw a semi-transparent red square
            Color(1, 0, 0, .5, mode='rgba')
            Rectangle(pos=self.pos, size=self.size)

        with self.canvas.before:
            Color(1, 0, .4, mode='rgb')
