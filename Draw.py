import time
import pygame
import sys
from Window import Window


# Creates the opening screne for maths td
def create_opening_animation(gameDisplay, screenWidth, screenHeight, sharedThreadVariable):
    font = pygame.font.Font("Data/comicsans.ttf", 100)
    text = font.render("Math-TD", True, (0, 128, 0))


    # Sets the x coordinate of the opening text
    xPos = int((screenWidth / 2) - (text.get_width() / 2))

    # Sets the ending y coordinate of the opening text
    endYPos = int(screenHeight/6)

    for i in range(-text.get_height(), endYPos):
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(text, (xPos, i))
        pygame.display.update()
        time.sleep(0.05)

        if sharedThreadVariable[0] != Window.IN_OPENING_SCENE:
            break

    # Draws the opening text into its final position
    gameDisplay.fill((0, 0, 0))
    gameDisplay.blit(text, (xPos, endYPos))
    
