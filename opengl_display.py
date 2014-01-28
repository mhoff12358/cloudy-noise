from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math, itertools

class OpenGLDisplay(object):
    def __init__(self, game, width=600, height=400, windowText="_"):
        self.game = game
        self.width = width
        self.height = height
        self.windowText = windowText
        self.window = None

    #PUBLIC FACING METHODS
    def setupView(self):
        self.setupGl()
        self.setupWindow()
        self.setupGlutCallbacks()

    def teardownView(self):
        self.teardownGlutCallbacks()
        self.teardownWindow()
        self.teardownGlutCallbacks()

    def resizeWindow(self, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)

    #INTERNAL METHODS
    def setupWindow(self):
        glutInit('')
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(0, 0)
        self.window = glutCreateWindow(self.windowText)
        glutReshapeFunc(self.resizeWindow)
        glDisable(GL_DEPTH_TEST)

    def teardownWindow(self):
        glutDestroyWindow(self.window)
        glutReshapeFunc(lambda: None)

    def setupGl(self):
        glClearColor(0.392, 0.584, 0.929, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_NEVER)
        glShadeModel(GL_SMOOTH)

    def teardownGl(self):
        pass

    def setupGlutCallbacks(self):
        glutDisplayFunc(self.drawScene)
        glutIdleFunc(self.drawScene)

    def teardownGlutCallbacks(self):
        glutDisplayFunc(lambda: None)
        glutIdleFunc(lambda: None)

    def drawScene(self):
        glClearColor(0.392, 0.584, 0.929, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.drawHexOverlay()

        glutSwapBuffers()

    def drawHexOverlay(self):
        hg = self.game.model

        glPushMatrix()
        glTranslate(-1, -1, 0)
        glScale(2./(hg.xsize-1.5), 2./(hg.ysize-1), 1)

        for y in range(hg.ysize-1):
            if y%2 == 0:
                fy = y+1
                sy = y
            else:
                fy = y
                sy = y+1
            firstheights = hg.heights[fy]
            secondheights = hg.heights[sy]
            glBegin(GL_TRIANGLE_STRIP)
            for x in range(len(firstheights)):
                glColor(firstheights[x].actual_height, 1, firstheights[x].actual_height)
                glVertex(x-.5, fy, 0)
                glColor(secondheights[x].actual_height, 1, secondheights[x].actual_height)
                glVertex(x, sy, 0)
            glEnd()
        glPopMatrix()
