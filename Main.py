import pygame
import sys

# Make program search in the src directory for files
sys.path.insert(1, './src')

import time
import threading
from Grid import Grid
from GameState import GameState
from Window import Window



current_window = None


def _initialise_pygame():
    """Initialises pygame and sets up a window"""
    global current_window

    pygame.init()
    pygame.display.set_caption('Maths TD')

    # Sets the background music
    song = pygame.mixer.Sound("Data/Music/ThisCharmingMan.wav")
    pygame.mixer.Sound.play(song, loops = -1)

    # Gets the resolution of the display that's running the game
    infoObject = pygame.display.Info()
    WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h
    GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialises the global window object
    current_window = Window(GAME_DISPLAY, WIDTH, HEIGHT)


# Main game loop for Maths-td
def _game_loop():
    global current_window

    gridSize = 10
    spawner_square = (5, 5)
    exit_square = (9, 9)
    grid = Grid(gridSize, gridSize, [], spawner_square, exit_square)
    clock = pygame.time.Clock()

    # Creates a thread lock that will run the opening animation
    lock = threading.Lock()

    # Starts the current window in the opening animation thread
    current_window.state = GameState.IN_OPENING_SCENE
    obj = current_window.start_opening_thread(lock)

    counter = 0
    # Handles events
    hasQuit = False
    while not hasQuit:
        pygame.display.update()

        for event in pygame.event.get():# + [pygame.event.wait()]:
            if event.type == pygame.QUIT:
                hasQuit = True
            
            # Deals with user inputs to the opening scene
            elif current_window.state == GameState.IN_OPENING_SCENE:
                current_window.process_opening_scene_event(event, lock)

            # Deals with user input in the main menu
            elif current_window.state == GameState.MAIN_MENU:
                current_window.process_main_menu_event(event, grid)

            # Deals with user input in game
            elif current_window.state == GameState.IN_GAME:
                current_window.process_in_game_event(event, grid)

        clock.tick(30)
        if current_window.state == GameState.IN_GAME and counter % 30 == 0:
            current_window.move_numemies(grid)
        counter += 1


if __name__ == "__main__":
    _initialise_pygame()
    _game_loop()
