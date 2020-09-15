import Draw
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
            highlightedButton = Button(rect, button.text, highlight)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = True
        elif button.highlighted:
            # Unhighlights the button when the mouse is no longer hovering over it
            highlight = (0, 0, 0)
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.text, highlight)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = False


def process_main_menu_click(window, mouseClickPos):
    """Processes the click event on the main menu"""

    for button in window.buttons:
        if button.rect.collidepoint(mouseClickPos):
           Draw.draw_initial_in_game_window(window)
           window.state = GameState.IN_GAME
