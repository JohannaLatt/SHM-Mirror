from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from rendering_widgets.skeleton_widget import SkeletonWidget

from random import random as r
from functools import partial
import json


# Define coordinate system that skeleton data arrives in
min_x = -2000
min_y = -2000
max_x = 2000
max_y = 2000


class GUIBase(App):

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.setJointData(data_str)

        '''self.skeleton_widget.canvas.clear()

        # Prepare the data
        data = json.loads(data_str)

        self.joint_data = data

        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2])
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2])

        print(self.joint_data)

        with self.skeleton_widget.canvas:
            for joint in self.joint_data:
                Color(0, 0, 1, mode='hsv')
                Line(points=
                        (self.rescale_joint_x_pos(joint[0][0]),
                        self.rescale_joint_y_pos(joint[0][1]),
                        self.rescale_joint_x_pos(joint[1][0]),
                        self.rescale_joint_y_pos(joint[1][1])),
                        width=7)
                Color(0, 1, 1, mode='hsv')
                self.draw_circle(self.rescale_joint_x_pos(joint[0][0]), self.rescale_joint_y_pos(joint[0][1]), 12)'''

    def clear_skeleton(self):
        self.skeleton_widget.canvas.clear()

    def test(self):
        with self.skeleton_widget.canvas:
            Color(r(), 1, 1, mode='hsv')
            self.draw_circle(150, 150, 30)
            Line(points=(0, 0, 150, 150, 300, 100), width=3)

    def draw_circle(self, x, y, diameter):
        Ellipse(pos=(x - diameter / 2, y - diameter/2), size=(diameter,diameter))

    def rescale_joint_x_pos(self, x):
        return ((x - min_x) / (max_x - min_x)) * self.skeleton_widget.width

    def rescale_joint_y_pos(self, y):
        return ((y - min_y) / (max_y - min_y)) * self.skeleton_widget.height

    def build(self):

        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        root = FloatLayout()
        root.add_widget(self.skeleton_widget)

        self.test()

        return root
