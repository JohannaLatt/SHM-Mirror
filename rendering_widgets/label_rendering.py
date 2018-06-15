from rendering_widgets.animated_label import AnimatedLabel

# ANIMATION
FADE_IN = "fade_in"
STAY = "stay"
FADE_OUT = "fade_out"


class LabelRenderer():

    def __init__(self, root):
        # Store the root to be able to add and remove labels
        self.root = root

        # Dict to store reused labels
        self.labels = {}

    def check_text_arguments(self, data):
        if "text" not in data:
            return False

        if "position" not in data:
            data["position"] = (0.5, 0.9)
        if "color" not in data:
            data["color"] = (1, 1, 1, 1)
        if "animation" not in data:
            data["animation"] = {}
            data["animation"]["fade_in"] = 2
            data["animation"]["stay"] = 5
            data["animation"]["fade_out"] = 2
        else:
            if "fade_in" not in data["animation"]:
                data["animation"]["fade_in"] = 2
            if "stay" not in data["animation"]:
                data["animation"]["stay"] = 5
            if "fade_out" not in data["animation"]:
                data["animation"]["fade_out"] = 2

        return True

    def show_static_text(self, data):
        # Check the data to make sure it has the necessary arguments
        is_valid_data = self.check_text_arguments(data)

        if not is_valid_data:
            print("[LabelRenderer][warning] Received invalid static text data - discarding")
            pass

        # Save the label's position
        x_pos = data["position"][0]
        y_pos = data["position"][1]

        # Check if there is an ID being sent, ie the label might exist already
        if "id" in data:
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
