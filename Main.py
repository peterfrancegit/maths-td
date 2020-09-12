import pygame
import grid
import Draw
import threading
from Window import Window

WIDTH = None
HEIGHT = None
GAME_DISPLAY = None
CURRENT_WINDOW = None
SHARED_THREAD_VARIABLE = []


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
    GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))


def run_opening_animation_thread():
    try:
        SHARED_THREAD_VARIABLE.append(CURRENT_WINDOW)
        t = threading.Thread(target = Draw.create_opening_animation, args=(GAME_DISPLAY, WIDTH, HEIGHT, SHARED_THREAD_VARIABLE))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)


# Main game loop for Maths-td
def _game_loop():
    global CURRENT_WINDOW

    gridSize = 10
    graph = grid.make_grid(gridSize, gridSize, [])
    clock = pygame.time.Clock()

    # Handles events
    hasQuit = False
    while not hasQuit:
        pygame.display.update()
        for event in pygame.event.get() + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True

            # On start up the opening scene is played
            elif CURRENT_WINDOW == None:
                CURRENT_WINDOW = Window.IN_OPENING_SCENE
                run_opening_animation_thread()

            # Deals with user inputs to the opening scene
            elif CURRENT_WINDOW == Window.IN_OPENING_SCENE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    CURRENT_WINDOW = Window.MAIN_MENU
                    SHARED_THREAD_VARIABLE[0] = CURRENT_WINDOW
        clock.tick(30)

if __name__ == "__main__":
    _initialise_pygame()
    _game_loop()