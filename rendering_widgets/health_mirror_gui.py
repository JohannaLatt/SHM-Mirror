from utils.enums import STATIC_TEXT_POSITIONS

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

from rendering_widgets.animation_label import AnimationLabel
from rendering_widgets.skeleton_gl_widget import SkeletonGLWidget

import json


class HealthMirrorGUI(QtWidgets.QWidget):

    def __init__(self, app, parent=None):
        super(HealthMirrorGUI, self).__init__(parent)

        self.static_text_views = {}
        self.dynamic_text_views = {}

        # Set geometry
        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height())
        self.setGeometry(geometry)

        # Button Section
        self.add_buttons()

        # Skeleton visualization
        self.skeletonWidget = SkeletonGLWidget()

        # Initialize statuc Text-views (invisible for now)
        for text_position in STATIC_TEXT_POSITIONS:
            self.static_text_views[text_position] = AnimationLabel()

        # Overall Layout
        self.layoutVertical = QtWidgets.QGridLayout(self)
        self.evenly_space_grid(self.layoutVertical, 3, 3, geometry)
        self.layoutVertical.addLayout(self.section_button, 2, 1)
        self.layoutVertical.addWidget(self.skeletonWidget, 0, 2)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # General settings
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

    @QtCore.pyqtSlot()
    def on_pushButtonClose_clicked(self):
        QtWidgets.QApplication.instance().quit()

    def evenly_space_grid(self, layout, cols, rows, geometry):
        for col in range(cols):
            layout.setColumnStretch(col, geometry.width() / cols)
        for row in range(rows):
            layout.setRowStretch(row, geometry.height() / rows)

    def add_buttons(self):
        self.section_button = QtWidgets.QGridLayout()

        # Close Button
        self.pushButtonClose = QtWidgets.QPushButton(self)
        self.pushButtonClose.setText("Close")
        self.pushButtonClose.clicked.connect(self.on_pushButtonClose_clicked)
        self.section_button.addWidget(self.pushButtonClose, 0, 1)

    def render_skeleton_data(self, data_str):
        self.skeletonWidget.setJointData(json.loads(data_str))

    def clear_skeleton(self):
        self.skeletonWidget.clear()

    def show_static_text(self, text, positioning='center'):
        # Check if there already is text at that position
        if self.text and self.text.positioning == positioning:
            self.text.fadeOut(.5)
            self.text.setText(text)
            self.show_text.fadeIn(1)
        else:
            pass
