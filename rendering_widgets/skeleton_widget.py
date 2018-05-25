from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse

import json


# Define coordinate system that skeleton data arrives in
min_x = -3000
min_y = -2000
max_x = 3000
max_y = 2000


class SkeletonWidget(Widget):

    def __init__(self, **kwargs):
        super(SkeletonWidget, self).__init__(**kwargs)

    def render_skeleton_data(self, data_str):
        # Clear the canvas
        self.canvas.clear()

        # Prepare the data
        self.joint_data = json.loads(data_str)

        # Convert the data to float
        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2])
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2])

        # Sort by depth - biggest value should be first, ie furthest away
        # so we can fake the 3D depth when rendering
        self.joint_data.sort(key=lambda x: x[1][2], reverse=True)

        # Render the data
        with self.canvas:
            for joint in self.joint_data:
                from_x = self.rescale_joint_x_pos(joint[0][0])
                from_y = self.rescale_joint_y_pos(joint[0][1])
                to_x = self.rescale_joint_x_pos(joint[1][0])
                to_y = self.rescale_joint_y_pos(joint[1][1])

                Color(0, 0, 1, 0.7, mode='hsv')
                Line(points=(from_x, from_y, to_x, to_y), width=3)

                Color(0, 1, 1, 0.7, mode='hsv')
                self.draw_circle(from_x, from_y, 14)
                self.draw_circle(to_x, to_y, 14)

    def clear_skeleton(self):
        self.canvas.clear()

    def draw_circle(self, x, y, diameter):
        Ellipse(pos=(x - diameter / 2, y - diameter/2), size=(diameter,diameter))

    def rescale_joint_x_pos(self, x):
        return ((x - min_x) / (max_x - min_x)) * self.width

    def rescale_joint_y_pos(self, y):
        return ((y - min_y) / (max_y - min_y)) * self.height
