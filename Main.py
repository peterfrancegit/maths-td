import pygame
import grid
import Draw

WIDTH = None
HEIGHT = None
GAME_DISPLAY = None


# Initialises pygame and sets up a window
def _initialise_pygame():
    global WIDTH
    global HEIGHT
    global GAME_DISPLAY

    pygame.init()
    pygame.display.set_caption('Maths TD')

    # Sets the background music
    song = pygame.mixer.Sound("Data/BackgroundMusic.wav")
    pygame.mixer.Sound.play(song, loops = -1)

    # Gets the resolution of the display that's running the game
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)


def _game_loop():
    Draw.create_opening_animation(GAME_DISPLAY, WIDTH, HEIGHT)
    gridSize = 10
    graph = grid.make_grid(gridSize, gridSize, [])
    clock = pygame.time.Clock()

    hasQuit = False
    while not hasQuit:
        pygame.display.update()
        for event in pygame.event.get() + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True
            else:
                pass
        clock.tick(30)

if __name__ == "__main__":
    _initialise_pygame()
    _game_loop()