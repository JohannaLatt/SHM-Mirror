from rendering_widgets.animated_label import AnimatedLabel

# ANIMATION
FADE_IN = "fade_in"
STAY = "stay"
FADE_OUT = "fade_out"


class LabelRenderer():

    def __init__(self, gui_base):
        # Store the root to be able to add and remove labels
        self.root = gui_base.root

        # Store the SkeletonWidget to be able to retrieve joint positions
        self.skeleton_widget = gui_base.skeleton_widget

        # Dict to store reused labels
        self.static_labels = {}

    def check_text_arguments(self, data):
        if "text" not in data:
            return False

        data["text"] = str(data["text"])

        if "font_size" not in data:
            data["font_size"] = 40
        if "halign" not in data:
            data["halign"] = "left"
        if "position" not in data:
            data["position"] = {"x": 0.5, "y": 0.9}
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

    def show_text(self, data):
        # Check the data to make sure it has the necessary arguments
        is_valid_data = self.check_text_arguments(data)

        if not is_valid_data:
            print("[LabelRenderer][warning] Received invalid static text data - discarding")
            pass

        # Calculate the label's position if it is dynamic
        if isinstance(data["position"], str):
            # Dynamic label at a joint's position
            pos = self.skeleton_widget.get_percentage_joint_pos(data["position"])
            x_pos = pos[0]
            y_pos = pos[1]

            # Slighlt adjust the text to the left or right so it's visible
            if "Left" in data["position"]:
                x_pos -= 0.015
            else:
                x_pos += 0.015
            data["position"] = {"x": x_pos, "y": y_pos}

            # We do NOT want the text bounding box to extend to the whole screen
            data["size_hint"] = (0, 0)
        else:
            # We do want the text bounding box to extend to the whole screen
            data["size_hint"] = (1, 1)

        # Check if there is an ID being sent, ie the label might exist already
        if "id" in data:
            # Label exists already
            if data["id"] in self.static_labels:
                label = self.static_labels[data["id"]]
                self.update_existing_label(label, data, data["position"])

            # We need a new label and save a reference to it via the ID
            else:
                label = AnimatedLabel(text=data["text"], pos_hint=data["position"], color=data["color"], font_size=data["font_size"], size_hint=data["size_hint"], halign=data["halign"])
                label.set_id(data["id"])
                self.static_labels[data["id"]] = label
                self.root.add_widget(label)
                self.animate_and_remove_label(label, {FADE_IN: data["animation"][FADE_IN], STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})

        # We need a new label that we do not need to save for later reference
        else:
            label = AnimatedLabel(text=data["text"], pos_hint=data["position"], color=data["color"], font_size=data["font_size"], size_hint=data["size_hint"], halign=data["halign"])
            self.root.add_widget(label)
            self.animate_and_remove_label(label, {FADE_IN: data["animation"][FADE_IN], STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})

    def update_existing_label(self, label, data, pos):
        # Stop possible animations
        label.cancel_animations()

        # Set the text and re-animate the text, skipping the fade-in
        label.set_text(data["text"])
        label.set_color(data["color"])
        label.set_pos_hint(pos)

        self.animate_and_remove_label(label, {FADE_IN: 0, STAY: data["animation"][STAY], FADE_OUT: data["animation"][FADE_OUT]})

    def animate_and_remove_label(self, label, animation_data):

        # Define function to remove label from root
        def remove_label(animation, label):
            self.root.remove_widget(label)

            # Remove reference to the label
            if label.get_id() in self.static_labels:
                self.delete_all_labels_with_id(label.get_id())
                del self.static_labels[label.get_id()]


        label.fade_in_and_out(animation_data[FADE_IN], animation_data[STAY], animation_data[FADE_OUT], remove_label)

    # For some reason, the remove_label callback is sometimes called for old
    # instances of a label which means the new instance doesn't actually get
    # deleted and stays on the screen. This helper makes sure that any
    # instance with a certain ID gets deleted, even if it is not referenced
    # in the static_labels-dict anymore
    def delete_all_labels_with_id(self, id):
        for w in self.root.children:
            if isinstance(w, AnimatedLabel) and w.get_id() == id:
                self.root.remove_widget(w)
