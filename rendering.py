from utils.enums import MSG_TO_MIRROR_KEYS

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QPoint, QSize, Qt
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QColor

from OpenGL.GL import *

import numpy as np

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
        self.axes.clear()

        data = json.loads(data_str)

        for pair in data:
            if len(pair) == 2:
                x_from_to = (float(pair[0][0]), float(pair[0][1]))
                y_from_to = (float(pair[1][0]), float(pair[1][1]))
                self.axes.plot(x_from_to, y_from_to, 'w-', lw=2)

                # Enforcing fixes axes
                self.axes.set_xlim([-1100, 1300])
                self.axes.set_ylim([-1100, 800])
            else:
                print('Invalid pair:{}'.format(str(pair)))

        self.skeleton_canvas.draw()

    def clear_skeleton(self):
        self.axes.clear()
        self.skeleton_canvas.draw()


class SkeletonGLWidget(QOpenGLWidget):

    joint_data = []

    def __init__(self, parent=None):
        super(SkeletonGLWidget, self).__init__(parent)

        self.skeleton = 0
        self.jointColor = QColor.fromCmykF(0.0, 0.0, 0.0, 0.0)

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

        #self.vertices = [0.0, 1.0, 0.0,  0.0, 0.0, 0.0,  1.0, 1.0, 0.0]
        self.vertices  = np.array([0.0, 1.0, 0.0,
                        0.0, 0.0, 0.0,
                        1.0, 1.0, 0.0], dtype=np.float32)
        self.vbo = self.gl.glGenBuffers (1)
        self.gl.glBindBuffer(self.gl.GL_ARRAY_BUFFER, self.vbo)
        #self.gl.glBufferData (self.gl.GL_ARRAY_BUFFER, len(self.vertices)*4, np.array (self.vertices, dtype="float32"), self.gl.GL_STATIC_DRAW)
        self.gl.glBufferData (self.gl.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, self.gl.GL_STATIC_DRAW)


    def paintGL(self):
        self.gl.glClear(
                self.gl.GL_COLOR_BUFFER_BIT | self.gl.GL_DEPTH_BUFFER_BIT)
        self.gl.glLoadIdentity()
        self.gl.glTranslated(0.0, 0.0, -10.0)
        # self.gl.glRotated(self.xRot / 16.0, 1.0, 0.0, 0.0)
        # self.gl.glRotated(self.yRot / 16.0, 0.0, 1.0, 0.0)
        # self.gl.glRotated(self.zRot / 16.0, 0.0, 0.0, 1.0)
        # self.gl.glCallList(self.makeSkeleton())
        self.makeSkeleton()

    '''def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        self.gl.glViewport((width - side) // 2, (height - side) // 2, side,
                side)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()
        self.gl.glOrtho(-0.5, +0.5, +0.5, -0.5, 4.0, 15.0)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW) '''

    def makeSkeleton(self):
        self.gl.glBindBuffer(self.gl.GL_ARRAY_BUFFER, self.vbo)
        self.gl.glVertexPointer(3, self.gl.GL_FLOAT, 0, None)

        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 3)

        '''genList = self.gl.glGenLists(1)
        self.gl.glNewList(genList, self.gl.GL_COMPILE)

        self.gl.glBegin(self.gl.GL_LINES)

        for joint in joint_data:


        x1 = +0.06
        y1 = -0.14
        x2 = +0.14
        y2 = -0.06
        x3 = +0.08
        y3 = +0.00
        x4 = +0.30
        y4 = +0.22

        self.quad(x1, y1, x2, y2, y2, x2, y1, x1)
        self.quad(x3, y3, x4, y4, y4, x4, y3, x3)

        self.extrude(x1, y1, x2, y2)
        self.extrude(x2, y2, y2, x2)
        self.extrude(y2, x2, y1, x1)
        self.extrude(y1, x1, x1, y1)
        self.extrude(x3, y3, x4, y4)
        self.extrude(x4, y4, y4, x4)
        self.extrude(y4, x4, y3, x3)

        NumSectors = 200

        for i in range(NumSectors):
            angle1 = (i * 2 * math.pi) / NumSectors
            x5 = 0.30 * math.sin(angle1)
            y5 = 0.30 * math.cos(angle1)
            x6 = 0.20 * math.sin(angle1)
            y6 = 0.20 * math.cos(angle1)

            angle2 = ((i + 1) * 2 * math.pi) / NumSectors
            x7 = 0.20 * math.sin(angle2)
            y7 = 0.20 * math.cos(angle2)
            x8 = 0.30 * math.sin(angle2)
            y8 = 0.30 * math.cos(angle2)

            self.quad(x5, y5, x6, y6, x7, y7, x8, y8)

            self.extrude(x6, y6, x7, y7)
            self.extrude(x8, y8, x5, y5)

        self.gl.glEnd()
        self.gl.glEndList()

        return genList'''

    def quad(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.setColor(self.trolltechGreen)

        self.gl.glVertex3d(x1, y1, -0.05)
        self.gl.glVertex3d(x2, y2, -0.05)
        self.gl.glVertex3d(x3, y3, -0.05)
        self.gl.glVertex3d(x4, y4, -0.05)

        self.gl.glVertex3d(x4, y4, +0.05)
        self.gl.glVertex3d(x3, y3, +0.05)
        self.gl.glVertex3d(x2, y2, +0.05)
        self.gl.glVertex3d(x1, y1, +0.05)

    def extrude(self, x1, y1, x2, y2):
        self.setColor(self.trolltechGreen.darker(250 + int(100 * x1)))

        self.gl.glVertex3d(x1, y1, +0.05)
        self.gl.glVertex3d(x2, y2, +0.05)
        self.gl.glVertex3d(x2, y2, -0.05)
        self.gl.glVertex3d(x1, y1, -0.05)

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())



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
            pass
        if view == MSG_TO_MIRROR_KEYS.CLEAR_SKELETON.name:
            gui.clear_skeleton()
        elif view == MSG_TO_MIRROR_KEYS.RENDER_SKELETON.name:
            gui.render_skeleton_data(data)
        else:
            print('[Rendering][warning] %r is not a suported view' % view)
