import Draw as Draw
import pygame
from Button import Button
from GameState import GameState
import Grid as Grid


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
                song = pygame.mixer.Sound("Data/Music/Girlfriendinacoma.wav")
                pygame.mixer.Sound.play(song, loops = -1)

                # Initialises the dijkstra and square grids
                Grid.initialise_grid(window.gameDisplay)

                Draw.draw_initial_in_game_window(window, Grid.square_grid)

                window.state = GameState.IN_GAME


            
            # Checks if the quit button has been pressed
            elif button.text == "Quit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))


def process_in_game_click(window, mouseClickPos):
    """Processes any left mouse clicks while in game"""

    for i, row in enumerate(Grid.square_grid):
        for j, sqr in enumerate(row):
            if sqr.surface.collidepoint(mouseClickPos):
                print(j, i)

