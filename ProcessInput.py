import Draw
import pygame
from Button import Button
from GameState import GameState
from Tower import Tower
from numemy import Numemy
import grid


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
            # Unhighlights the button when the mouse is no longer hovering over it
            highlight = (0, 0, 0)
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.font, highlight, button.text)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = False


def process_main_menu_click(window, mouseClickPos):
    """Checks if any of the buttons in the window have been clicked on"""

    for button in window.buttons:
        if button.rect.collidepoint(mouseClickPos):

            # Checks if the start button has been pressed
            if button.text == "Start":

                # Changes the music
                pygame.mixer.stop()
                song = pygame.mixer.Sound("Data/Girlfriendinacoma.wav")
                pygame.mixer.Sound.play(song, loops = -1)

                # Initialises the dijkstra and square grids
                grid.initialise_grid(window.gameDisplay)

                # Creates a numemy with the value 6 and puts it into square_grid
                sqr = grid.square_grid[4][0]
                w, h = sqr.surface.width, sqr.surface.height
                rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
                grid.square_grid[4][0] = Numemy(rect, 6, 0, 3, [])

                # Creates a numemy with the value 3 and puts it into square_grid
                sqr = grid.square_grid[4][1]
                w, h = sqr.surface.width, sqr.surface.height
                rect = pygame.Rect(sqr.surface.x, sqr.surface.y, w, h)
                grid.square_grid[4][1] = Numemy(rect, 3, 0, 3, [])

                Draw.draw_initial_in_game_window(window, grid.square_grid)

                window.state = GameState.IN_GAME


            
            # Checks if the quit button has been pressed
            elif button.text == "Quit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))


def process_in_game_click(window, mouseClickPos):
    """Processes any left mouse clicks while in game"""

    for i, row in enumerate(grid.square_grid):
        for j, sqr in enumerate(row):
            if sqr.surface.collidepoint(mouseClickPos):
                print(j, i)

