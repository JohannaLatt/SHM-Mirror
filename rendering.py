from enum import Enum
from PyQt5 import QtCore, QtWidgets
import messaging as Messaging
from messaging import MSG_FROM_MIRROR_KEYS
import sys
import time
import threading


class VIEWS(Enum):
    TEXT = 1
    SKELETON = 2


class HealthMirrorGUI(QtWidgets.QWidget):

    def __init__(self, app, parent=None):
        super(HealthMirrorGUI, self).__init__(parent)

        # Sample data
        self.stop_simulating = threading.Event()
        self.sample_tracking_data = open('./data/sample-tracking-data.txt').read().splitlines()
        self.simulation_thread = threading.Thread(target=self.simulate_tracking)

        # Start-Mirror Button
        self.pushButtonStartMirror = QtWidgets.QPushButton(self)
        self.pushButtonStartMirror.setText("Start Mirror")
        self.pushButtonStartMirror.clicked.connect(self.on_pushButtonMirrorStarted_clicked)

        # Simulate Tracking Button
        self.pushButtonSimulateTracking = QtWidgets.QPushButton(self)
        self.pushButtonSimulateTracking.setText("Simulate Tracking")
        self.pushButtonSimulateTracking.clicked.connect(self.on_pushButtonSimulateTracking_clicked)

        self.pushButtonStopSimulating = QtWidgets.QPushButton(self)
        self.pushButtonStopSimulating.setText("Stop Simulating Tracking")
        self.pushButtonStopSimulating.clicked.connect(self.on_pushButtonStopSimulating_clicked)

        # Close Button
        self.pushButtonClose = QtWidgets.QPushButton(self)
        self.pushButtonClose.setText("Close")
        self.pushButtonClose.clicked.connect(self.on_pushButtonClose_clicked)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.pushButtonStartMirror)
        self.layoutVertical.addWidget(self.pushButtonSimulateTracking)
        self.layoutVertical.addWidget(self.pushButtonStopSimulating)
        self.layoutVertical.addWidget(self.pushButtonClose)

        titleBarHeight = self.style().pixelMetric(
            QtWidgets.QStyle.PM_TitleBarHeight,
            QtWidgets.QStyleOptionTitleBar(),
            self
        )

        geometry = app.desktop().availableGeometry()
        geometry.setHeight(geometry.height() - (titleBarHeight*2))

        self.setGeometry(geometry)

    @QtCore.pyqtSlot()
    def on_pushButtonMirrorStarted_clicked(self):
        Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_READY.name, '')

    @QtCore.pyqtSlot()
    def on_pushButtonSimulateTracking_clicked(self):
        Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_TRACKING_STARTED.name, '')
        self.simulation_thread.start()

    @QtCore.pyqtSlot()
    def on_pushButtonStopSimulating_clicked(self):
        self.stop_simulating.set()

    @QtCore.pyqtSlot()
    def on_pushButtonClose_clicked(self):
        QtWidgets.QApplication.instance().quit()

    def simulate_tracking(self):
        for tracking_data_item in self.sample_tracking_data:
            if not self.stop_simulating.is_set():
                Messaging.send(MSG_FROM_MIRROR_KEYS.MIRROR_TRACKING_DATA.name, tracking_data_item)
                time.sleep(.5)
        self.stop_simulating.clear()


def init_gui():
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Smart Health Mirror')

    main = HealthMirrorGUI(app)
    main.show()

    sys.exit(app.exec_())


def render(view, data):
    if view == VIEWS.TEXT:
        pass
    elif view == VIEWS.SKELETON:
        pass
    else:
        print('[warning] %r is not a suported view' % view)
