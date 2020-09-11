import time
import pygame


# Creates the opening screne for maths td
def create_opening_animation(gameDisplay, screenWidth, screenHeight):
    font = pygame.font.Font("Data/comicsans.ttf", 100)
    text = font.render("Math-TD", True, (0, 128, 0))


    # Sets the x coordinate of the opening text
    xPos = int((screenWidth / 2) - (text.get_width() / 2))

    # Sets the ending y coordinate of the opening text
    endYPos = int(screenHeight/4)
    for i in range(-text.get_height(), endYPos):
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(text, (xPos, i))
        pygame.display.update()
        time.sleep(0.05)
