#!/usr/bin/env python

#Imports!
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from OpenGL.GL import shaders

from opengl_display import OpenGLDisplay
from pygame_display import PygameDisplay
from control import Controller
from cloudy import CloudGrid

from pygame.locals import *

import pygame

class Game(object):
    def __init__(self):
        # self.view = OpenGLDisplay(self, width=1200, height=600)
        self.view = PygameDisplay(self, width=1200, height=1000)
        self.controller = Controller(self)
        self.model = CloudGrid(self)

        self.setupUniverse()

    def setupUniverse(self):
        self.view.setupView()
        # self.controller.setupController()

        # glutMainLoop()
        clock = pygame.time.Clock()
        while 1:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return

            self.view.drawScene()

    def teardownUniverse(self):
        # self.controller.teardownController()
        self.view.teardownView()

        exit()

if __name__ == "__main__":
    g = Game()