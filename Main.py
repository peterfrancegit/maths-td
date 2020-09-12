import pygame
import grid
import Draw
from GameState import GameState
from Window import Window


CURRENT_WINDOW = None

# Mouse buttons
LEFT = 1
RIGHT = 3


# Initialises pygame and sets up a window
def _initialise_pygame():
    global WIDTH
    global HEIGHT
    global GAME_DISPLAY
    global CURRENT_WINDOW

    pygame.init()
    pygame.display.set_caption('Maths TD')

    # Sets the background music
    song = pygame.mixer.Sound("Data/BackgroundMusic.wav")
    pygame.mixer.Sound.play(song, loops = -1)

    # Gets the resolution of the display that's running the game
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialises the global window object
    CURRENT_WINDOW = Window(GAME_DISPLAY, WIDTH, HEIGHT)



# Main game loop for Maths-td
def _game_loop():
    global CURRENT_WINDOW

    gridSize = 10
    graph = grid.make_grid(gridSize, gridSize, [])
    clock = pygame.time.Clock()

    #pygame.event.post(pygame.event.Event(pygame.USEREVENT))
    # Handles events
    hasQuit = False
    while not hasQuit:
        for event in pygame.event.get():# + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True

            # On start up the opening scene is played
            elif CURRENT_WINDOW.state == None:
                CURRENT_WINDOW.state = GameState.IN_OPENING_SCENE
                CURRENT_WINDOW.run_opening_animation_thread()

            # Deals with user inputs to the opening scene
            elif CURRENT_WINDOW.state == GameState.IN_OPENING_SCENE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    CURRENT_WINDOW = GameState.MAIN_MENU

            # Deals with user input in the main menu
            elif CURRENT_WINDOW.state == GameState.MAIN_MENU:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    mouseClickPos = pygame.mouse.get_pos()
        clock.tick(30)

if __name__ == "__main__":
    _initialise_pygame()
    _game_loop()