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
        # Define function to remove label from root
        def remove_label(animation, label):
            self.root.remove_widget(label)

            # Remove reference to the label
            if label.get_id() in self.labels:
                del self.labels[label.get_id()]

        # Check if there is an ID being sent, ie the label might exist already
        if kwargs["id"] is not None:
            if kwargs["id"] in self.labels:
                label = self.labels[kwargs["id"]]

                # Stop possible animations
                label.cancel_animations()

                # Set the text and re-animate the text, skipping the fade-in
                label.set_text(kwargs["text"])
                label.set_color(kwargs["color"])
                label.fade_in_and_out(0, kwargs["animation"]["stay"], kwargs["animation"]["fade_out"], remove_label)
            else:
                label = AnimatedLabel(text=kwargs["text"], pos_hint={"x": kwargs["position"][0], "y": kwargs["position"][1]}, color=kwargs["color"])
                label.set_id(kwargs["id"])
                self.labels[kwargs["id"]] = label
                self.root.add_widget(label)

                label.fade_in_and_out(kwargs["animation"]["fade_in"], kwargs["animation"]["stay"], kwargs["animation"]["fade_out"], remove_label)
        else:
            label = AnimatedLabel(text=kwargs["text"], pos_hint={"x": kwargs["position"][0], "y": kwargs["position"][1]}, color=kwargs["color"])
            self.root.add_widget(label)

            label.fade_in_and_out(kwargs["animation"]["fade_in"], kwargs["animation"]["stay"], kwargs["animation"]["fade_out"], remove_label)

    def build(self):
        # Dict to store reused labels
        self.labels = {}

        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        self.root = FloatLayout()
        self.root.add_widget(self.skeleton_widget)

        return self.root
