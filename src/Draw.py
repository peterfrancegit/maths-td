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
    # Red for messages
    elif weight == 8:
        return (255, 0, 0)
    # For Bronze level 1 Tower
    elif weight == 9:
        return (173, 138, 86)
    # For silver level 2 Tower
    elif weight == 10:
        return (180, 180, 180)
    # For gold level 3 Tower
    elif weight == 11:
        return (201, 176, 55)


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
            pygame.draw.rect(display, font_colour(object.level + 8), square[0].surface)
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
    draw_side_menu(window, grid)
    draw_message_box(window, grid)
    draw_souls_box(window, grid)


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
    """Draws the menu with buttons for in-game"""
    menuTop = grid.square_grid[0][0][0].surface.bottom
    menuLeft = grid.square_grid[0][0][0].surface.left / 10
    menuHeight = grid.square_grid[0][0][0].surface.height * (grid.height - 2)
    menuWidth = menuLeft * 8
    menuColour = (0, 0, 100)
    menuRect = pygame.Rect(menuLeft, menuTop, menuWidth, menuHeight)
    pygame.draw.rect(window.gameDisplay, menuColour, menuRect)
    buttHeight = menuHeight / 10
    buttWidth = menuWidth / 2
    buttX = menuLeft + menuWidth / 4
    buttY = menuTop + 4 * menuHeight / 5
    # Make empty Button for input of the value of a Tower to buy
    fontSize = get_fitted_size("", buttWidth, buttHeight)
    font = create_font_object("", fontSize, 7)
    rect = pygame.Rect(buttX, buttY, buttWidth, buttHeight)
    window.input = Button(rect, font, (0, 0, 0), "")
    # Make other Buttons
    labels = ["Buy", "Upgrade", "Sell", "+", "-", "*", "/"]
    for i in range(7):
        buttY = menuTop + i * menuHeight / 5
        if i >= 3:
            buttWidth = menuWidth / 8
            buttX = menuLeft + (i - 1) * menuWidth / 8
            buttY = menuTop + 3 * menuHeight / 5
        text = labels[i]
        fontSize = get_fitted_size(text, buttWidth, buttHeight)
        font = create_font_object(text, fontSize, 7)
        rect = pygame.Rect(buttX, buttY, buttWidth, buttHeight)
        if i in [1, 2]:
            window.sellButtons.append(Button(rect, font, menuColour, text))
        else:
            window.buyButtons.append(Button(rect, font, menuColour, text))
    # Draw all the Buttons
    draw_menu(window, window.sellButtons + window.buyButtons + [window.input])

    
def draw_message_box(window, grid):
    """Draws the box where messages will be displayed"""
    boxTop = grid.square_grid[grid.height // 2][0][0].surface.bottom
    boxLeft = grid.square_grid[0][0][0].surface.left / 10 + grid.square_grid[0][-1][0].surface.right
    boxHeight = grid.square_grid[0][0][0].surface.height * (grid.height // 2 - 2)
    boxWidth = 8 * grid.square_grid[0][0][0].surface.left / 10
    boxColour = (100, 100, 100)
    boxRect = pygame.Rect(boxLeft, boxTop, boxWidth, boxHeight)
    fontSize = get_fitted_size("", boxWidth, boxHeight)
    font = create_font_object("", fontSize, 8)
    window.message_box = Button(boxRect, font, (100, 100, 100), "")
    draw_button(window, window.message_box)

def draw_souls_box(window, grid):
    """Draws a box to display the current amount of souls"""
    boxTop = grid.square_grid[0][0][0].surface.bottom
    boxLeft = grid.square_grid[0][0][0].surface.left / 10 + grid.square_grid[0][-1][0].surface.right
    boxHeight = grid.square_grid[0][0][0].surface.height
    boxWidth = 8 * grid.square_grid[0][0][0].surface.left / 10
    boxColour = (100, 0, 0)
    boxRect = pygame.Rect(boxLeft, boxTop, boxWidth, boxHeight)
    text = "Souls: " + str(grid.souls)
    fontSize = get_fitted_size(text, boxWidth, boxHeight)
    font = create_font_object(text, fontSize, 7)
    window.souls_box = Button(boxRect, font, boxColour, text)
    draw_button(window, window.souls_box)

def draw_range_circle(window, grid, position):
    """Draws a circle representing the range of a Tower"""
    square = grid.square_grid[position[0]][position[1]]
    squareSideLen = square[0].surface.width
    circleX = int(square[0].surface.x + squareSideLen / 2)
    circleY = int(square[0].surface.y + squareSideLen / 2)
    pygame.draw.circle(window.gameDisplay, (255, 0 , 0), (circleX, circleY), square[1].range)
