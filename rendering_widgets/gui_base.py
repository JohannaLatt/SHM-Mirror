from kivy.config import Config

Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'width', '1700')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', 0)

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window

from rendering_widgets.skeleton_widget import SkeletonWidget
from rendering_widgets.label_rendering import LabelRenderer


class GUIBase(App):

    # Init (called by kivy)
    def build(self):
        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        self.root = FloatLayout()
        self.root.add_widget(self.skeleton_widget)

        # Initalize the module that takes care of the label rendering
        self.label_renderer = LabelRenderer(self)

        return self.root

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.render_skeleton_data(data_str)

    def change_joint_or_bone_color(self, data_str):
        self.skeleton_widget.color_bone_or_joint(data_str)

    def clear_skeleton(self):
        self.skeleton_widget.clear_skeleton()

    def show_static_text(self, data):
        self.label_renderer.show_static_text(data)
