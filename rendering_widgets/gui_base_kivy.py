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


# ANIMATION
FADE_IN = "fade_in"
STAY = "stay"
FADE_OUT = "fade_out"


class GUIBase(App):

    # Init (called by kivy)
    def build(self):
        # Dict to store reused labels
        self.labels = {}

        # Fullscreen widget to draw the skeleton
        self.skeleton_widget = SkeletonWidget()

        self.root = FloatLayout()
        self.root.add_widget(self.skeleton_widget)

        return self.root

    def render_skeleton_data(self, data_str):
        self.skeleton_widget.render_skeleton_data(data_str)

    def clear_skeleton(self):
        self.skeleton_widget.clear_skeleton()

    def show_text(self, data):
        # Save the label's position
        x_pos = data["position"][0]
        y_pos = data["position"][1]

        # Check if there is an ID being sent, ie the label might exist already
        if data["id"] is not None:
            # Labels exists already
            if data["id"] in self.labels:
                label = self.labels[data["id"]]
                self.update_existing_label(label, data)
            # We need a new label and save a reference to it via the ID
            else:
                label = AnimatedLabel(text=data["text"], pos_hint={"x": x_pos, "y": y_pos}, color=data["color"])
                label.set_id(data["id"])
                self.labels[data["id"]] = label
                self.root.add_widget(label)
                self.animate_and_remove_label(label, {FADE_IN: data["animation"][FADE_IN], STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})
        # We need a new label that we do not need to save for later reference
        else:
            label = AnimatedLabel(text=data["text"], pos_hint={"x": x_pos, "y": y_pos}, color=data["color"])
            self.root.add_widget(label)
            self.animate_and_remove_label(label, {FADE_IN: data["animation"][FADE_IN], STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})

    def update_existing_label(self, label, data):
        # Stop possible animations
        label.cancel_animations()

        # Set the text and re-animate the text, skipping the fade-in
        label.set_text(data["text"])
        label.set_color(data["color"])

        self.animate_and_remove_label(label, {FADE_IN: 0, STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})

    def animate_and_remove_label(self, label, animation_data):

        # Define function to remove label from root
        def remove_label(animation, label):
            self.root.remove_widget(label)

            # Remove reference to the label
            if label.get_id() in self.labels:
                del self.labels[label.get_id()]

        label.fade_in_and_out(animation_data[FADE_IN], animation_data[STAY], animation_data[FADE_OUT], remove_label)
