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
        self.drawOverlay()

        pygame.display.flip()

    def drawOverlay(self):
        hg = self.game.model
        pixel = pygame.Surface((5, 5))

        for x in range(hg.get_size(0)):
            for y in range(hg.get_size(1)):
                if hg.get_center(x, y):
                    pixel.fill((0, 0, 0))
                else:
                    if int(hg.get_height(x, y)*255) == 0:
                        pixel.fill((0, 0, 255))
                    else:
                        pixel.fill((int(hg.get_height(x, y)*255), 255, int(255*hg.get_height(x, y))))
                self.window.blit(pixel, (5*x, 5*y))

        for x in range(len(hg.hist)):
            col_width = int(self.width/len(hg.hist))
            pixel = pygame.Surface((col_width, hg.hist[x]))
            pixel.fill((255, 0, 0))
            self.window.blit(pixel, (col_width*x, self.game.view.height-hg.hist[x]))

