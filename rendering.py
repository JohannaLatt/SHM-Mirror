from enum import Enum

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import messaging as Messaging
from messaging import MSG_FROM_MIRROR_KEYS
import sys
import time
import threading

import random


class VIEWS(Enum):
    TEXT = 1
    RENDER_SKELETON = 2


class HealthMirrorGUI(QtWidgets.QWidget):

    def __init__(self, app, parent=None):
        super(HealthMirrorGUI, self).__init__(parent)

        # Set geometry
        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height())
        self.setGeometry(geometry)

        # Button Section
        self.add_buttons()

        # Skeleton visualization
        fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = fig.add_subplot(122)
        self.skeleton_canvas = FigureCanvas(fig)

        FigureCanvas.updateGeometry(self)
        data = [random.random() for i in range(25)]
        self.axes.plot(data, 'r-')
        self.skeleton_canvas.draw()

        # Overall Layout
        self.layoutVertical = QtWidgets.QGridLayout(self)
        self.evenly_space_grid(self.layoutVertical, 3, 3, geometry)
        self.layoutVertical.addLayout(self.section_button, 2, 1)
        self.layoutVertical.addWidget(self.skeleton_canvas, 1, 1)

        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # General settings
        self.showMaximized()
        self.setWindowFlags(Qt.FramelessWindowHint)

    @QtCore.pyqtSlot()
    def on_pushButtonMirrorStarted_clicked(self):
        Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_READY.name, '')

    @QtCore.pyqtSlot()
    def on_pushButtonClose_clicked(self):
        QtWidgets.QApplication.instance().quit()

    def simulate_tracking(self):
        for tracking_data_item in self.sample_tracking_data:
            if not self.stop_simulating.is_set():
                Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_TRACKING_DATA.name, tracking_data_item)
                time.sleep(.5)
        self.stop_simulating.clear()

    def evenly_space_grid(self, layout, cols, rows, geometry):
        for col in range(cols):
            layout.setColumnStretch(col, geometry.width() / cols)
        for row in range(rows):
            layout.setRowStretch(row, geometry.height() / rows)

    def add_buttons(self):
        self.section_button = QtWidgets.QGridLayout()

        # Start-Mirror Button
        self.pushButtonStartMirror = QtWidgets.QPushButton(self)
        self.pushButtonStartMirror.setText("Start Mirror")
        self.pushButtonStartMirror.clicked.connect(self.on_pushButtonMirrorStarted_clicked)
        self.section_button.addWidget(self.pushButtonStartMirror, 0, 0)

        # Close Button
        self.pushButtonClose = QtWidgets.QPushButton(self)
        self.pushButtonClose.setText("Close")
        self.pushButtonClose.clicked.connect(self.on_pushButtonClose_clicked)
        self.section_button.addWidget(self.pushButtonClose, 0, 1)

    def render_skeleton_data(self, data):
        print('Rendering {}'.format(data))
        #self.axes.plot(x_pair, y_pair, zs=z_pair, linewidth=3)
        pass


def init_gui():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Smart Health Mirror')

    global main
    main = HealthMirrorGUI(app)
    main.show()

    sys.exit(app.exec_())


def render(view, data):
    if view == VIEWS.TEXT:
        pass
    elif view == VIEWS.RENDER_SKELETON.name:
        if main:
            main.render_skeleton_data(data)
        else:
            print('[Rendering][warning] Message discarded, rendering not initialized yet')
    else:
        print('[Rendering][warning] %r is not a suported view' % view)
