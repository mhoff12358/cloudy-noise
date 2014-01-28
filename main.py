#!/usr/bin/env python

#Imports!
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

from opengl_display import OpenGLDisplay
from control import Controller
from hexgrid import HexGrid

class Game(object):
    def __init__(self):
        self.view = OpenGLDisplay(self, width=1200, height=600)
        self.controller = Controller(self)
        self.model = HexGrid(self)

        self.setupUniverse()

    def setupUniverse(self):
        self.view.setupView()
        self.controller.setupController()

        glutMainLoop()

    def teardownUniverse(self):
        self.controller.teardownController()
        self.view.teardownView()

        exit()

if __name__ == "__main__":
    g = Game()