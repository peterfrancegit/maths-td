import Draw
import pygame
from Button import Button


def process_main_menu_hover(window, mouseClickPos):
    for button in window.buttons:
        if button.rect.collidepoint(mouseClickPos):
            # Creates the highlighted button
            highlight = (200,200,100)
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
