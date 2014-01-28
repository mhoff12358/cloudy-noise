from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Controller(object):
    def __init__(self, game):
        self.game = game


    #PUBLIC FACING METHODS
    def setupController(self):
        self.setupIOCalls()

    def teardownController(self):
        self.teardownIOCalls()

    #INTERNAL METHODS
    def startTimer(self):
        glutTimerFunc(1000/60, self.timerUpdate, 0)

    def timerUpdate(self, value):
        self.startTimer()

    def keyboardPress(self, *args):
        if args[0] == '\033':
            self.game.teardownUniverse()
            sys.exit()

    def keyboardUpPress(self, *args):
        if args[0] == '\033':
            pass

    def mouseMotion(self, x, y):
        pass

    def setupIOCalls(self):
        glutKeyboardFunc(self.keyboardPress)
        glutKeyboardUpFunc(self.keyboardUpPress)
        glutIgnoreKeyRepeat(True)

        glutPassiveMotionFunc(self.mouseMotion)

        self.startTimer()

    def teardownIOCalls(self):
        glutKeyboardFunc(lambda: None)
        glutKeyboardUpFunc(lambda: None)

        glutPassiveMotionFunc(lambda: None)

        self.startTimer()