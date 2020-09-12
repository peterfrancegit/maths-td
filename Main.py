import pygame
import grid
import Draw
from GameState import GameState
import Window

WIDTH = None
HEIGHT = None
GAME_DISPLAY = None
CURRENT_WINDOW = None
SHARED_THREAD_VARIABLE = []

# Mouse buttons
LEFT = 1
RIGHT = 3


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
                CURRENT_WINDOW = GameState.IN_OPENING_SCENE
                SHARED_THREAD_VARIABLE.append(CURRENT_WINDOW)
                Window.run_opening_animation_thread(GAME_DISPLAY, WIDTH, HEIGHT, SHARED_THREAD_VARIABLE)
                print("Hello")

            # Deals with user inputs to the opening scene
            elif CURRENT_WINDOW == GameState.IN_OPENING_SCENE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    CURRENT_WINDOW = GameState.MAIN_MENU
                    SHARED_THREAD_VARIABLE[0] = CURRENT_WINDOW

            # Deals with user input in the main menu
            elif CURRENT_WINDOW == GameState.MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    print("Hello")
        clock.tick(30)

if __name__ == "__main__":
    _initialise_pygame()
    _game_loop()