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


class GUIBase(App):

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.render_skeleton_data(data_str)

    def clear_skeleton(self):
        self.skeleton_widget.clear_skeleton()

    def build(self):
        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        root = FloatLayout()
        root.add_widget(self.skeleton_widget)

        return root
