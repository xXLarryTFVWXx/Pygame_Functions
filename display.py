import os, pygame

screenRefresh = False

class Window:
    def __init__(self, sizex, sizey, xpos=None, ypos=None, bg_color="black", fullscreen=False):
        self.sizex = sizex
        self.sizey = sizey
        self.xpos = xpos
        self.ypos = ypos
        self.fullscreen = fullscreen
        self.bg_color = parseColour(bg_color)
        self.screen = None
    def create(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode((self.sizex, self.sizey), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.sizex, self.sizey))
    def clear(self):
        self.screen.fill(self.bg_color)
    def blit(self, surface, x, y, subsurface=None):
        if subsurface is None:
            self.screen.blit(surface, (x, y))
        else:
            self.screen.blit(surface, (x, y), subsurface)

    def refresh(self):
        pygame.display.flip()
    def close(self):
        pygame.display.quit()


def parseColour(colour):
    # is the colour an instance of str?
    if isinstance(colour, str):
        return pygame.Color(colour)
    if isinstance(colour, (list, tuple)):
        if len(colour) < 3:
            raise IndexError("Not enough values in colour list")
        if len(colour) > 4:
            raise IndexError("Too many values in colour list")
        return pygame.Color(*colour)
    if isinstance(colour, pygame.Color):
        return colour
    raise TypeError(f"Colour is invalid, expected string, list or tuple, got {type(colour)}")

def loadImage(fileName, useColorKey=False, colorKey=None):
    if os.path.isfile(fileName):
        # automatically convert the image to the display format
        image = pygame.image.load(fileName).convert_alpha()
        if useColorKey and not colorKey is None:
            # set the color key for the image
            image.set_colorkey(parseColour(colorKey))
        return image
    if os.path.isdir(fileName):
        raise IsADirectoryError()
    raise FileNotFoundError(f"File {fileName} not found")

def makeImage(filename):
    return loadImage(filename)

class Background():
    def __init__(self, screen=""):
        self.colour = pygame.Color("black")
        self.screen = screen

    def setTiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[loadImage(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[loadImage(i) for i in tiles]]
        else:
            self.tiles = [[loadImage(i) for i in row] for row in tiles]
        self.stagePosX = 0
        self.stagePosY = 0
        self.tileWidth = self.tiles[0][0].get_width()
        self.tileHeight = self.tiles[0][0].get_height()
        self.screen.blit(self.tiles[0][0], [0, 0])
        self.surface = self.screen.copy()

    def scroll(self, x, y):
        """ Will refactor after I have a better understanding of how this works """
        self.stagePosX -= x
        self.stagePosY -= y
        col = (self.stagePosX % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        xOff = (0 - self.stagePosX % self.tileWidth)
        row = (self.stagePosY % (self.tileHeight * len(self.tiles))) // self.tileHeight
        yOff = (0 - self.stagePosY % self.tileHeight)

        col2 = ((self.stagePosX + self.tileWidth) % (self.tileWidth * len(self.tiles[0]))) // self.tileWidth
        row2 = ((self.stagePosY + self.tileHeight) % (self.tileHeight * len(self.tiles))) // self.tileHeight
        self.screen.blit(self.tiles[row][col], [xOff, yOff])
        self.screen.blit(self.tiles[row][col2], [xOff + self.tileWidth, yOff])
        self.screen.blit(self.tiles[row2][col], [xOff, yOff + self.tileHeight])
        self.screen.blit(self.tiles[row2][col2], [xOff + self.tileWidth, yOff + self.tileHeight])

        self.surface = self.screen.copy()
    def resize(self, x, y, width, height, fullscreen=False) -> None:
        if fullscreen:
            self.screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
            return None
        self.screen = pygame.display.set_mode((width, height))
    def setColour(self, colour):
        self.colour = parseColour(colour)
        self.screen.fill(self.colour)
        pygame.display.update()
        self.surface = self.screen.copy()

def screenSize(sizex, sizey, xpos=None, ypos=None, fullscreen=False):
    global screen
    global background
    if xpos != None and ypos != None:
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{xpos}, {ypos + 50}"
    else:
        windowInfo = pygame.display.Info()
        monitorWidth = windowInfo.current_w
        monitorHeight = windowInfo.current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{(monitorWidth - sizex) // 2}, {(monitorHeight - sizey) // 2}"
    if fullscreen:
        screen = pygame.display.set_mode([sizex, sizey], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([sizex, sizey])
    background = Background()
    screen.fill(background.colour)
    pygame.display.set_caption("Graphics Window")
    background.surface = screen.copy()
    pygame.display.update()
    return screen


