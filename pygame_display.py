import pygame

class PygameDisplay(object):
    def __init__(self, game, width=600, height=400, windowText="_"):
        self.game = game
        self.width = width
        self.height = height
        self.windowText = windowText
        self.window = None
        self.pixel_size = 5

    #PUBLIC FACING METHODS
    def setupView(self):
        self.setupPygame()
        self.setupWindow()

    def teardownView(self):
        self.teardownWindow()

    def resizeWindow(self, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    	self.window = pygame.display.set_mode((self.width, self.height))

    #INTERNAL METHODS
    def setupWindow(self):
    	self.window = pygame.display.set_mode((self.width, self.height))
    	pygame.display.set_caption(self.windowText)

    def teardownWindow(self):
    	pass

    def setupPygame(self):
    	pygame.init()

    def teardownPygame(self):
        pass

    def drawScene(self):
        self.drawHexOverlay()

        pygame.display.flip()

    def drawHexOverlay(self):
        hg = self.game.model
        pixel = pygame.Surface((5, 5))

        for x in range(hg.xsize):
        	for y in range(hg.ysize):
        		pixel.fill((int(hg.retrieve_height(x, y).actual_height*255), 255, int(255*hg.retrieve_height(x, y).actual_height)))
        		self.window.blit(pixel, (5*x, 5*y))

