from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QColor

from OpenGL.GLUT import glutSolidSphere


class SkeletonGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(SkeletonGLWidget, self).__init__(parent)

        self.skeleton = 0
        self.boneColor = QColor.fromRgbF(1.0, 1.0, 1.0, 0.0)
        self.jointColor = QColor.fromRgbF(1.0, 0.36, 0.36, 0.0)

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
        self.gl.glTranslated(0.0, 0.0, -2000.0)
        self.gl.glCallList(self.drawSkeleton())
        self.drawJoints()

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        self.gl.glViewport((width - side) // 2, (height - side) // 2, side, side)

        self.gl.glMatrixMode(self.gl.GL_PROJECTION)
        self.gl.glLoadIdentity()

        # Left, right, bottom, top, zNear, zFar
        self.gl.glOrtho(-2000, 2000, -2000, 2000, -500, 7000)
        self.gl.glMatrixMode(self.gl.GL_MODELVIEW)

    # Draws Lines
    def drawSkeleton(self):
        genList = self.gl.glGenLists(1)
        self.gl.glNewList(genList, self.gl.GL_COMPILE)
        self.setColor(self.boneColor)
        self.gl.glLineWidth(10)

        self.gl.glBegin(self.gl.GL_LINES)

        for joint in self.joint_data:
            self.gl.glVertex3d(joint[0][0], joint[0][1], joint[0][2])  # from
            self.gl.glVertex3d(joint[1][0], joint[1][1], joint[1][2])  # to
            # print("({} {} {}) -> ({} {} {})".format(joint[0][0], joint[0][1], joint[0][2], joint[1][0], joint[1][1], joint[1][2]))

        self.gl.glEnd()
        self.gl.glEndList()

        return genList

    # Draws Joints
    def drawJoints(self):
        self.gl.glLoadIdentity()
        self.setColor(self.jointColor)
        for joint in self.joint_data:
            self.gl.glTranslated(joint[0][0], joint[0][1], joint[0][2] - 2000)
            glutSolidSphere(20,20,20)
            self.gl.glLoadIdentity()

    def setClearColor(self, c):
        self.gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        self.gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setJointData(self, data):
        self.joint_data = data

        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2])
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2])

        self.update()

    def clear(self):
        self.joint_data = []
        self.update()
