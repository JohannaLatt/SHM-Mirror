from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Ellipse
from kivy.core.window import Window

from collections import deque

# Define coordinate system that skeleton data arrives in
min_x = -1200  # based on window-width of 1700
min_y = -1000  # based on window-height of 900
max_x = 2200
max_y = 1000


class SkeletonWidget(Widget):

    def __init__(self, **kwargs):
        super(SkeletonWidget, self).__init__(**kwargs)
        self.joints = []
        self.bones = []
        self.joint_colors = {}
        self.bone_colors = {}

        self.line_width = 3
        self.circle_diameter = 18
        self.default_bone_color = (0, 0, 1, 0.9)
        self.default_joint_color = (0, 0, 0.4, 0.8)

        # Adapt the coordinate system according to the screen size
        self.last_foot_y_min = deque(maxlen=5)
        self.min_x = min_x * (Window.size[0] / 1700)
        self.min_y = min_y * (Window.size[1] / 900)
        self.max_x = max_x * (Window.size[0] / 1700)
        self.max_y = max_y * (Window.size[1] / 900)

    def render_skeleton_data(self, data):
        # Clear the canvas
        self.canvas.clear()

        # Prepare the data
        self.joints = data['Joints']
        self.bones = data['Bones']

        # Save lowest foot position
        lowest_foot_position = min(self.joints['FootRight'][1], self.joints['FootLeft'][1])
        self.last_foot_y_min.append(lowest_foot_position)
        self.adjust_bottom_of_screen()

        # Scale the joint coordinates to screen coordinates
        for joint, joint_position in self.joints.items():
            self.joints[joint] = [
                self.rescale_joint_x_pos(joint_position[0]),
                self.rescale_joint_y_pos(joint_position[1]), joint_position[2]
            ]

        # Sort the joints by depth (z) - biggest value should be first, ie
        # furthest away so we can fake the 3D depth when rendering
        sorted_bones = sorted(
            self.bones.keys(),
            key=lambda bone: self.joints[self.bones[bone][0]][2],
            reverse=True)

        # Render the data
        with self.canvas:
            for sorted_bone in sorted_bones:
                bone_joints = self.bones[sorted_bone]
                from_x = self.joints[bone_joints[0]][0]
                from_y = self.joints[bone_joints[0]][1]
                to_x = self.joints[bone_joints[1]][0]
                to_y = self.joints[bone_joints[1]][1]

                # Draw the bone
                color = self.get_bone_color(sorted_bone)
                Color(color[0], color[1], color[2], color[3], mode='hsv')
                Line(points=(from_x, from_y, to_x, to_y), width=self.line_width)

                # Draw the from-joint
                color = self.get_joint_color(bone_joints[0])
                Color(color[0], color[1], color[2], color[3], mode='hsv')
                self.draw_circle(from_x, from_y, self.circle_diameter)

                # Draw the to-joint
                color = self.get_joint_color(bone_joints[1])
                Color(color[0], color[1], color[2], color[3], mode='hsv')
                self.draw_circle(to_x, to_y, self.circle_diameter)

    def clear_skeleton(self):
        self.canvas.clear()

    def get_bone_color(self, bone):
        if bone in self.bone_colors:
            return self.bone_colors[bone]
        return self.default_bone_color

    def get_joint_color(self, joint):
        if joint in self.joint_colors:
            return self.joint_colors[joint]
        return self.default_joint_color

    def color_bone_or_joint(self, data):
        # Get the data
        type = data['type'].lower()
        name = data['name']
        color = data['color']

        # Checks
        if type != 'bone' and type != 'joint':
            print("[SkeletonWidget][warning] Type has to be 'joint' or 'bone', not {}".format(type))
            pass

        if not isinstance(color, list) or len(color) is not 4:
            if type == 'bone':
                color = self.default_bone_color
            elif type == 'joint':
                color = self.default_joint_color

        if type is 'bone' and type not in self.bone_lines:
            print("[SkeletonWidget][warning] Bone {} does not exist, cannot change color.".format(name))
            pass

        elif type is 'joint' and type not in self.joint_circles:
            print("[SkeletonWidget][warning] Joint {} does not exist, cannot change color.".format(name))
            pass

        # Save color for next rendering call
        if type == 'bone':
            self.bone_colors[name] = color
        elif type == 'joint':
            self.joint_colors[name] = color

    def draw_circle(self, x, y, diameter):
        return Ellipse(
            pos=(x - diameter / 2, y - diameter / 2),
            size=(diameter, diameter))

    def rescale_joint_x_pos(self, x):
        return ((x - self.min_x) / (self.max_x - self.min_x)) * self.width

    def adjust_bottom_of_screen(self):
        if len(self.last_foot_y_min) == self.last_foot_y_min.maxlen:
            self.min_y = min(self.last_foot_y_min)

    def rescale_joint_y_pos(self, y):
        return ((y - self.min_y) / (self.max_y - self.min_y)) * self.height

    def get_percentage_joint_pos(self, joint):
        if joint in self.joints:
            x_pos = self.joints[joint][0]
            y_pos = self.joints[joint][1]

            return [x_pos / self.width, y_pos / self.height]
        return [0,0]
