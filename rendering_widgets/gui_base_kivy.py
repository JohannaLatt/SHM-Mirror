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
from rendering_widgets.animated_label import AnimatedLabel


class GUIBase(App):

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.render_skeleton_data(data_str)

    def clear_skeleton(self):
        self.skeleton_widget.clear_skeleton()

    def show_text(self, **kwargs):
        label = AnimatedLabel(text=kwargs["text"], pos_hint={"x": kwargs["position"][0], "y": kwargs["position"][1]})
        self.root.add_widget(label)

        def remove_label(event, anim):
            self.root.remove_widget(label)

        label.fade_in_and_out(kwargs["animation"]["fade_in"], kwargs["animation"]["stay"], kwargs["animation"]["fade_out"], remove_label)

    def build(self):
        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        self.root = FloatLayout()
        self.root.add_widget(self.skeleton_widget)

        return self.root
