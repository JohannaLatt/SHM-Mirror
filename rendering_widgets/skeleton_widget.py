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
        data = json.loads(data_str)
        self.joints = data['Joints']
        self.bones = data['Bones']

        # Scale the joint coordinates to screen coordinates
        for joint, joint_position in self.joints.items():
            self.joints[joint] = [self.rescale_joint_x_pos(joint_position[0]),
                                  self.rescale_joint_y_pos(joint_position[1]),
                                  joint_position[2]]

        # Sort the joints by depth (z) - biggest value should be first, ie
        # furthest away so we can fake the 3D depth when rendering
        sorted_bones = sorted(self.bones.keys(), key=lambda bone: self.joints[self.bones[bone][0]][2], reverse=True)

        # Render the data
        with self.canvas:
            for sorted_bone in sorted_bones:
                bone_joints = self.bones[sorted_bone]
                from_x = self.joints[bone_joints[0]][0]
                from_y = self.joints[bone_joints[0]][1]
                to_x = self.joints[bone_joints[1]][0]
                to_y = self.joints[bone_joints[1]][1]

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
