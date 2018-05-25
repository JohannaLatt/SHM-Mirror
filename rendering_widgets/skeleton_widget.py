from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.resources import resource_find

from kivy.graphics.opengl import *
from kivy.graphics import *

from OpenGL.GL import *


class SkeletonWidget(Widget):

    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        super(SkeletonWidget, self).__init__(**kwargs)
        with self.canvas:
            self.setup_scene()

    def setup_scene(self):
        glClearColor(0, 0, 0, 0)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Left, right, bottom, top, zNear, zFar
        glOrtho(-2000, 2000, -2000, 2000, -1500, 7000)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslated(0.0, 0.0, -2000.0)
        glCallList(self.drawSkeleton())
        #drawJoints()
        self.canvas.ask_update()

    def draw_skeleton(self):
        glGenLists(1)
        glNewList(genList, GL_COMPILE)
        glColor4f(1, 1, 1, 0)
        glLineWidth(5)

        glUseProgram(0)
        glBegin(GL_LINES)

        for joint in self.joint_data:
            glVertex3d(joint[0][0], joint[0][1], joint[0][2])  # from
            glVertex3d(joint[1][0], joint[1][1], joint[1][2])  # to
            # print("({} {} {}) -> ({} {} {})".format(joint[0][0], joint[0][1], joint[0][2], joint[1][0], joint[1][1], joint[1][2]))

        glEnd()
        glEndList()

        return genList

    def setJointData(self, data):
        self.joint_data = data

        for joint in self.joint_data:
            joint[0][0] = float(joint[0][0])
            joint[0][1] = float(joint[0][1])
            joint[0][2] = float(joint[0][2])
            joint[1][0] = float(joint[1][0])
            joint[1][1] = float(joint[1][1])
            joint[1][2] = float(joint[1][2])

        self.paintGL()
