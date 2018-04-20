from utils.enums import MSG_TO_MIRROR_KEYS

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QColor

import json

import messaging as Messaging
from messaging import MSG_FROM_MIRROR_KEYS
import sys
import time


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
        self.skeletonWidget = SkeletonGLWidget()

        # Overall Layout
        self.layoutVertical = QtWidgets.QGridLayout(self)
        self.evenly_space_grid(self.layoutVertical, 3, 3, geometry)
        self.layoutVertical.addLayout(self.section_button, 2, 1)
        self.layoutVertical.addWidget(self.skeletonWidget, 1, 1)

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

    def render_skeleton_data(self, data_str):
        self.skeletonWidget.setJointData(json.loads(data_str))

    def clear_skeleton(self):
        self.axes.clear()
        self.skeleton_canvas.draw()


class SkeletonGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(SkeletonGLWidget, self).__init__(parent)

        self.skeleton = 0
        self.jointColor = QColor.fromCmykF(0.0, 0.0, 0.0, 0.0)

        self.joint_data = []

    def minimumSizeHint(self):
        return QSize(50, 50)

    def sizeHint(self):
        return QSize(400, 400)

    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.initializeOpenGLFunctions()

        self.setClearColor(QColor.fromCmykF(1.0, 1.0, 1.0, 0.0))
        self.gl.glShadeModel(self.gl.GL_FLAT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glEnable(self.gl.GL_CULL_FACE)

    def paintGL(self):
        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(0.0, 0.0, 0.0)
        self.gl.glCallList(self.makeSkeleton())

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        #self.gl.glOrtho(left, right, bottom, top, zNear, zFar)
        self.gl.glOrtho(-900, 950, -1400, 900, -500, 1500.0)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)

    def makeSkeleton(self):
        genList = self.gl.glGenLists(1)
        self.gl.glNewList(genList, self.gl.GL_COMPILE)
        self.setColor(self.jointColor)

        self.gl.glBegin(self.gl.GL_LINES)

        self.gl.glLineWidth(200)

        for joint in self.joint_data:
            self.gl.glVertex3d(joint[0][0], joint[0][1], joint[0][2])  # from
            self.gl.glVertex3d(joint[1][0], joint[1][1], joint[1][2])  # to

        self.gl.glEnd()
        self.gl.glEndList()

        return genList

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setJointData(self, data):
        self.joint_data = data

        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2]) - 2000
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2]) - 2000

        self.update()


def init_gui():
    print('[Rendering][info] Initializing GUI')
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Smart Health Mirror')

    global gui
    gui = HealthMirrorGUI(app)
    gui.show()

    sys.exit(app.exec_())


def render(view, data):
    try:
        gui
    except NameError:
        print('[Rendering][warning] Message discarded, rendering not initialized yet')
    else:
        if view == MSG_TO_MIRROR_KEYS.TEXT.name:
            print(data)
        elif view == MSG_TO_MIRROR_KEYS.CLEAR_SKELETON.name:
            gui.clear_skeleton()
        elif view == MSG_TO_MIRROR_KEYS.RENDER_SKELETON.name:
            gui.render_skeleton_data(data)
        else:
            print('[Rendering][warning] %r is not a suported view' % view)
