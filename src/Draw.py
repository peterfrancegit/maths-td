import time
import pygame
import sys
from GameState import GameState
from Square import Square, Block, Exit, Spawner
from Tower import Tower
from Numemy import Numemy
from Button import Button
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

def font_colour(weight):
    # For level 1 Numemy
    if weight == 1:
        return (153, 251, 55)
    # For level 2 Numemy
    elif weight == 2:
        return (0, 128, 255)
    # For level 3 Numemy
    elif weight == 3:
        return (0, 0, 102)
    # For level 4 Numemy
    elif weight == 4:
        return (51, 0, 51)
    # For level 5 Numemy
    elif weight == 5:
        return (0, 0, 0)
    # For Exit and Towers
    elif weight == 6:
        return (251, 251, 251)
    # The classic Maths TD colour
    elif weight == 7:
        return (0, 128, 0)


def create_font_object(text, size, weight):
    """Takes a string and produces a pygame text object with it and return that object"""
    font = pygame.font.Font("Data/Fonts/Oswald-Regular.ttf", size)
    fontobj = font.render(text, True, font_colour(weight))
    return fontobj


def get_fitted_size(text, width, height):
    """Takes a piece of text and the side of an area and gets the max size of text that can fit the area"""
    counter = 1
    font = create_font_object(text, counter, 1)
    w, h = font.get_size()
    while (w < width and h < height):
        font = create_font_object(text, counter, 1)
        w, h = font.get_size()
        counter += 1
    
    # Reducing counter by 1 will give the last text size that could fit in the surface
    counter -= 1
    if counter == 0:
        raise TextTooBig("Text can not be fitted to the given surface")
    else:
        return counter
    

def draw_square(window, square, spawnerSqr):
    """Draws each object in a square unto the display object"""

    display = window.gameDisplay
    numemyInSpawn = False
    for object in square:
        if isinstance(object, Tower):
            pygame.draw.rect(display, (32, 15, 100), square[0].surface)
            text = object.operation + str(object.value)
            surfaceWidth = square[0].surface.width
            surfaceHeight = square[0].surface.height
            size = get_fitted_size(text, surfaceWidth, surfaceHeight)
            font = create_font_object(text, size, 6)
            w, h = font.get_size()
            textX = square[0].surface.x + ((square[0].surface.width - w) / 2)
            textY = square[0].surface.y + ((square[0].surface.height - h) / 2)
            display.blit(font, (textX, textY))
        elif isinstance(object, Block):
            pygame.draw.rect(display, (139, 69, 19), square[0].surface)
        elif isinstance(object, Numemy):
            if object.location == spawnerSqr:
                if not numemyInSpawn:
                    numemyInSpawn = True
                else:
                    continue
            text = str(object.value)
            surfaceWidth = square[0].surface.width
            surfaceHeight = square[0].surface.height
            size = get_fitted_size(text, surfaceWidth, surfaceHeight)
            font = create_font_object(text, size, object.weight)
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

            # Draws the circle
            squareSideLen = square[0].surface.width
            circleX = int(square[0].surface.x + squareSideLen / 2)
            circleY = int(square[0].surface.y + squareSideLen / 2)
            radius = int(square[0].surface.width / 2)
            pygame.draw.circle(display, (255, 0, 0), (circleX, circleY), radius, 0)

            # Draws the value of the exit
            text = str(object.value)
            surfaceWidth = square[0].surface.width
            surfaceHeight = square[0].surface.height
            size = get_fitted_size(text, surfaceWidth, surfaceHeight)
            font = create_font_object(text, size, 6)
            w, h = font.get_size()
            widthLengthDiff = int(square[0].surface.width - w)
            heightLengthDiff = int(square[0].surface.height - h)
            display.blit(font, (square[0].surface.x + widthLengthDiff / 2, square[0].surface.y + heightLengthDiff / 2))

        elif isinstance(object, Square):

            colour = None
            if not object is window.selectedEntity["square"]:
                colour = (128, 128, 128)
            else:
                colour = (0,255,255)

            # Draws background
            pygame.draw.rect(display, colour, square[0].surface)
            pygame.draw.rect(display, (0, 0, 0), square[0].surface, 1)

def draw_initial_in_game_window(window, grid):
    """Draws the initial in game window"""

    screenWidth, screenHeight = window.gameDisplay.get_size()

    # Draws a black background
    window.gameDisplay.fill((0, 0, 0))

    # Draws each of the squares in square_grid
    for i in range(len(grid.square_grid)):
        for j in range(len(grid.square_grid[0])):
            draw_square(window, grid.square_grid[i][j], grid.spawner_square)


def draw_squares(window, grid, squaresToDraw):
    """Takes a list of square positions in squareGrid which will be redrawn later"""
    for pos in squaresToDraw:
        draw_square(window, grid.square_grid[pos[0]][pos[1]], grid.spawner_square)


def draw_game_over(display, screenRatio):
    """Draws the game over screen"""

    # Draws the game of text
    text = "Game Over"
    size = int(200 * screenRatio)
    font = create_font_object(text, size)
    fontWidth, fontHeight = font.get_size()
    screenWidth, screenHeight = display.get_size()
    display.blit(font, (screenWidth / 2 - fontWidth / 2, screenHeight / 2 - fontHeight / 2))

def draw_side_menu(window, grid):
    if window.selectedEntity["square"] != None:
        square = grid.square_grid[window.selectedEntity["position"][0]][window.selectedEntity["position"][1]]
        menuHeight = window.gameDisplay.get_size()[1] * 19 / 20
        menuWidth = (window.gameDisplay.get_size()[1] - (square[0].surface.width * grid.width)) * 35
        menuTop = menuHeight / 30
        menuLeft = menuWidth / 35
        menuColour = (0, 0, 0)
        menuRect = pygame.Rect(menuLeft, menuTop, menuWidth, menuHeight)
        pygame.draw.rect(window.gameDisplay, menuColour, menuRect)
        if len(square) == 1:
            draw_buy_menu(window, menuRect, menuColour)
        else:
            draw_sell_menu(window, menuRect, menuColour)

def draw_buy_menu(window, menuRect, menuColour):
    menuHeight = menuRect.height
    menuWidth = menuRect.width
    buttons = []
    buttHeight = menuHeight / 10
    labels = ["Purchase", "+", "-", "*", "/", "Value:"]
    for i in range(6):
        if i in [0, 5]:
            buttWidth = menuWidth / 2
            buttX = menuWidth / 4
            if i == 0:
                buttY = menuHeight / 5
            else:
                buttY = 3 * menuHeight / 5
        else:
            buttWidth = menuWidth / 8
            buttX = i * menuWidth / 6
            buttY = 4 * menuHeight / 5
        text = labels[i]
        fontSize = get_fitted_size(text, buttWidth, buttHeight)
        font = create_font_object(text, fontSize, 7)
        rect = pygame.Rect(buttX, buttY, buttWidth, buttHeight)
        buttons.append(Button(rect, font, menuColour, text))
    draw_menu(window, buttons)


def draw_sell_menu(window, menuRect, menuColour):
    menuHeight = menuRect.height
    menuWidth = menuRect.width
    buttons = []
    colour = (0, 0, 0)
    buttHeight = menuHeight / 10
    buttWidth = menuWidth / 2
    buttX = menuWidth / 4
    labels = ["Upgrade", "Sell"]
    for i in range(2):
        if i == 0:
            buttY = menuHeight / 5
        else:
            buttY = 3 * menuHeight / 5
        text = labels[i]
        fontSize = get_fitted_size(text, buttWidth, buttHeight)
        font = create_font_object(text, fontSize, 7)
        rect = pygame.Rect(buttX, buttY, buttWidth, buttHeight)
        buttons.append(Button(rect, font, menuColour, text))
    draw_menu(window, buttons)
