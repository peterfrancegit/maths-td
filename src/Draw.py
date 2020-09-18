import time
import pygame
import sys
from GameState import GameState
from Square import Square, Block, Exit
from Tower import Tower
from Numemy import Numemy


def create_opening_animation(window, lock):
    """Creates the opening screen for maths td"""

    lock.acquire() # Locks is used from thread communication

    font = pygame.font.Font("Data/Fonts/comicsans.ttf", 100 * window.screenRatio)
    textSurface = font.render("Math-TD", True, (0, 128, 0))


    # Sets the x coordinate of the opening text
    xPos = int((window.width / 2) - (textSurface.get_width() / 2))

    # Sets the ending y coordinate of the opening text
    endYPos = int(window.height / 6)

    skip = False
    for i in range(-textSurface.get_height(), endYPos):
        window.gameDisplay.fill((0, 0, 0))
        window.gameDisplay.blit(textSurface, (xPos, i))
        pygame.display.update()
        time.sleep(0.05)

        if window.state != GameState.IN_OPENING_SCENE:
            break


    # Draws the opening text into its final position
    window.gameDisplay.fill((0, 0, 0))
    window.gameDisplay.blit(textSurface, (xPos, endYPos))

    pygame.display.update()

    lock.release()


def draw_button(window, button):
    """Draws a button on to the game display"""
    pygame.draw.rect(window.gameDisplay, button.colour, button.rect)
    window.gameDisplay.blit(button.font, (button.rect.x, button.rect.y))


def draw_image(display, imagename, x, y):
    """Draws an image specified on the given x y coordinates"""
    numbers = pygame.image.load("./Data/Images/" + imagename)
    display.blit(numbers, (x, y))

def draw_menu(window, buttons):
    """Draws all of the buttons specified in buttons"""
    for button in buttons:
        draw_button(window, button)


def create_font_object(text, size):
    """Takes a string and produces a pygame text object with it and return that object"""
    font = pygame.font.Font("Data/Fonts/comicsans.ttf", size)
    fontobj = font.render(text, True, (0, 128, 0))
    return fontobj


def draw_square(display, square):
    """Draws the square object unto the display object"""

    if isinstance(square, Numemy):
        pygame.draw.rect(display, (128, 128, 128), square.surface)
        text = str(square.value)
        size = square.surface.height - 15
        font = create_font_object(text, size)
        w, h = font.get_size()
        display.blit(font, (square.surface.x + w / 2, square.surface.y))

    elif isinstance(square, Tower):
        pygame.draw.rect(display, (32, 15, 100), square.surface)
        text = square.operation + str(square.value)
        size = square.surface.height - 30
        font = create_font_object(text, size)
        w, h = font.get_size()
        display.blit(font, (square.surface.x + w / 2, square.surface.y))

    elif isinstance(square, Block):
        pygame.draw.rect(display, (200, 13, 52), square.surface)

    elif isinstance(square, Exit):
        # Draws the background of the exit
        pygame.draw.rect(display, (128, 128, 128), square.surface)

        # Draws the exit
        squareSideLen = square.surface.width
        circleX = int(square.surface.x + squareSideLen / 2)
        circleY = int(square.surface.y + squareSideLen / 2)
        radius = int(square.surface.width / 2)
        pygame.draw.circle(display, (255, 0, 0), (circleX, circleY), radius, 0)

    elif isinstance(square, Square):
        pygame.draw.rect(display, (128, 128, 128), square.surface)


def draw_initial_in_game_window(window, grid):
    """Draws the initial in game window"""

    screenWidth, screenHeight = window.gameDisplay.get_size()

    # Draws a black background
    window.gameDisplay.fill((0, 0, 0))

    # Draws a grey square at the centre of the screen
    # greySqrWidth = screenHeight
    # greySqrHeight = screenHeight
    # greySqrX = screenWidth / 2 - greySqrWidth / 2
    # greySqrY = 0
    # greySqr = pygame.Rect(greySqrX, greySqrY, greySqrWidth, greySqrHeight)
    # pygame.draw.rect(window.gameDisplay, (128, 128, 128), greySqr)

    for i in range(len(grid)):
        for j in range(len(grid)):
            draw_square(window.gameDisplay, grid[i][j])

    
