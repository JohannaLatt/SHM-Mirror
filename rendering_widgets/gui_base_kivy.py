from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'width', '1700')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Line, Color, Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from random import random as r
from functools import partial
import json


# Define coordinate system that skeleton data arrives in
min_x = -3000
min_y = -2000
max_x = 3000
max_y = 2000


class GUIBase(App):

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.canvas.clear()

        # Prepare the data
        data = json.loads(data_str)

        self.joint_data = data

        # Convert the data to float
        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2])
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2])

        # Sort by depth - biggest value should be first, ie furthest away
        self.joint_data.sort(key=lambda x: x[1][2], reverse=True)

        print(self.joint_data)
        # Render the data - draw bones first and then the joints so they overlap the joints
        with self.skeleton_widget.canvas:
            for joint in self.joint_data:
                from_x = self.rescale_joint_x_pos(joint[0][0])
                from_y = self.rescale_joint_y_pos(joint[0][1])
                to_x = self.rescale_joint_x_pos(joint[1][0])
                to_y = self.rescale_joint_y_pos(joint[1][1])

                Color(0, 0, 1, mode='hsv')
                Line(points=(from_x, from_y, to_x, to_y), width=3)

                Color(0, 1, 1, mode='hsv')
                self.draw_circle(from_x, from_y, 14)
                self.draw_circle(to_x, to_y, 14)

    def clear_skeleton(self):
        self.skeleton_widget.canvas.clear()

    def draw_circle(self, x, y, diameter):
        Ellipse(pos=(x - diameter / 2, y - diameter/2), size=(diameter,diameter))

    def rescale_joint_x_pos(self, x):
        return ((x - min_x) / (max_x - min_x)) * self.skeleton_widget.width

    def rescale_joint_y_pos(self, y):
        return ((y - min_y) / (max_y - min_y)) * self.skeleton_widget.height

    def build(self):

        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = Widget()

        root = FloatLayout()
        root.add_widget(self.skeleton_widget)

        return root
