import time
import pygame
import sys
from GameState import GameState
from Square import Square, Block, Exit, Spawner
from Tower import Tower
from Numemy import Numemy
from Exceptions.TextTooBig import TextTooBig


def create_opening_animation(window, lock):
    """Creates the opening screen for maths td"""

    lock.acquire() # Locks is used from thread communication

    font = pygame.font.Font("Data/Fonts/Oswald-Regular.ttf", int(100 * window.screenRatio))
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
    font = pygame.font.Font("Data/Fonts/Oswald-Regular.ttf", size)
    fontobj = font.render(text, True, (0, 128, 0))
    return fontobj


def get_fitted_size(text, surface):
    """Takes a piece of text and a surface and gets the max size of text that can fit the surface"""
    counter = 1
    font = create_font_object(text, counter)
    w, h = font.get_size()
    while (w < surface.width and h < surface.height):
        font = create_font_object(text, counter)
        w, h = font.get_size()
        counter += 1
    
    # Reducing counter by 1 will give the last text size that could fit in the surface
    counter -= 1
    if counter == 0:
        raise TextTooBig("Text can not be fitted to the given surface")
    else:
        return counter
    

def draw_square(display, square):
    """Draws each object in a square unto the display object"""
    for object in square:
        if isinstance(object, Tower):
            pygame.draw.rect(display, (32, 15, 100), square[0].surface)
            text = square[0].operation + str(square[0].value)
            size = get_fitted_size(text, square[0].surface)
            font = create_font_object(text, size)
            w, h = font.get_size()
            textX = square[0].surface.x + ((square[0].surface.width - w) / 2)
            textY = square[0].surface.y + ((square[0].surface.height - h) / 2)
            display.blit(font, (textX, textY))

        elif isinstance(object, Block):
            pygame.draw.rect(display, (139, 69, 19), square[0].surface)

        elif isinstance(object, Square):
            # Draws background
            pygame.draw.rect(display, (128, 128, 128), square[0].surface)
            pygame.draw.rect(display, (0, 0, 0), square[0].surface, 1)
            if isinstance(object, Numemy):
                text = str(object.value)
                size = get_fitted_size(text, square[0].surface)
                font = create_font_object(text, size)
                w, h = font.get_size()
                widthLengthDiff = int(square[0].surface.width - w)
                heightLengthDiff = int(square[0].surface.height - h)
                display.blit(font, (square[0].surface.x + widthLengthDiff / 2, square[0].surface.y + heightLengthDiff / 2))
            elif isinstance(object, Spawner):
                squareSideLen = square[0].surface.width
                circleX = int(square[0].surface.x + squareSideLen / 2)
                circleY = int(square[0].surface.y + squareSideLen / 2)
                radius = int(square[0].surface.width / 2)
                pygame.draw.circle(display, (255, 255, 0), (circleX, circleY), radius, 0)
            elif isinstance(object, Exit):
                squareSideLen = square[0].surface.width
                circleX = int(square[0].surface.x + squareSideLen / 2)
                circleY = int(square[0].surface.y + squareSideLen / 2)
                radius = int(square[0].surface.width / 2)
                pygame.draw.circle(display, (255, 0, 0), (circleX, circleY), radius, 0)


def draw_initial_in_game_window(window, squareGrid):
    """Draws the initial in game window"""

    screenWidth, screenHeight = window.gameDisplay.get_size()

    # Draws a black background
    window.gameDisplay.fill((0, 0, 0))

    # Draws each of the squares in square_grid
    for i in range(len(squareGrid)):
        for j in range(len(squareGrid[0])):
            draw_square(window.gameDisplay, squareGrid[i][j])


def draw_squares(window, squareGrid, squaresToDraw):
    """Takes a list of square positions in squareGrid which will be redrawn later"""
    for pos in squaresToDraw:
        draw_square(window.gameDisplay, squareGrid[pos[0]][pos[1]])

    
