from abc import ABC, abstractmethod


class AbstractGUIBase(ABC):

    @abstractmethod
    def render_skeleton_data(self, data_str):
        pass

    @abstractmethod
    def change_joint_or_bone_color(self, data_str):
        pass

    @abstractmethod
    def clear_skeleton(self):
        pass

    @abstractmethod
    def show_text(self, data):
        pass

    @abstractmethod
    def update_graps(self, data):
        pass
