import Draw as Draw
import pygame
from Button import Button
from GameState import GameState


def process_main_menu_hover(window, mouseClickPos):
    """Processes the hover event on the main menu"""

    for button in window.buttons:
        if button.rect.collidepoint(mouseClickPos):
            # Creates the highlighted button
            highlight = (255,140,0)
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.font, highlight, button.text)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = True
        elif button.highlighted:
            # Lowlights the button when the mouse is no longer hovering over it
            highlight = (0, 0, 0)
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.font, highlight, button.text)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = False


def process_main_menu_click(window, mouseClickPos, grid):
    """Checks if any of the buttons in the window have been clicked on"""

    for button in window.buttons:
        if button.rect.collidepoint(mouseClickPos):

            # Checks if the start button has been pressed
            if button.text == "Start":

                # Changes the music
                pygame.mixer.stop()
                song = pygame.mixer.Sound("Data/Music/Girlfriendinacoma.wav")
                pygame.mixer.Sound.play(song, loops = -1)

                # Initialises the square_grid
                grid.initialise_square_grid(window.gameDisplay)
                # Initialises any blocks
                grid.initialise_blocks()
                # Adds the Exit
                grid.initialise_exit()
                # Adds the Spawner
                grid.initialise_spawner()
                # Initialises the dijk_grid
                grid.initialise_dijk_grid()
                # Initialises the route_dict
                grid.initialise_route_dict()

                # Adds a Numemy
                grid.spawn_numemy(10, 10, 10, 10)
                grid.spawn_numemy(20, 10, 10, 10)

                Draw.draw_initial_in_game_window(window, grid.square_grid)

                window.state = GameState.IN_GAME

            # Checks if the quit button has been pressed
            elif button.text == "Quit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))


def process_in_game_click(window, mouseClickPos, grid):
    """Processes any left mouse clicks while in game"""

    for i, row in enumerate(grid.square_grid):
        for j, sqr in enumerate(row):
            if len(sqr) == 1 and (i, j) not in grid.forbidden_squares:
                if sqr[0].surface.collidepoint(mouseClickPos):
                    grid.build_tower(3, 2, 1, "-", 5, (i, j))
                    grid.update_routes()
                    grid.update_forbidden_squares()
                    Draw.draw_squares(window, grid.square_grid, [(i, j)])
