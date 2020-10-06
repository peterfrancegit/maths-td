import Draw as Draw
import pygame
from Button import Button
from GameState import GameState


def process_menu_hover(window, mouseClickPos, button_list):
    """Processes the hover event on the main menu"""

    for button in button_list:
        if button.rect.collidepoint(mouseClickPos):
            # Creates the highlighted button
            highlight = (255,140,0)
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.font, highlight, button.text)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = True
        elif button.highlighted:
            # Lowlights the button when the mouse is no longer hovering over it

            highlight = button.colour
            rect = pygame.Rect(button.rect.x, button.rect.y, button.rect.width, button.rect.height)
            highlightedButton = Button(rect, button.font, highlight, button.text)

            Draw.draw_button(window, highlightedButton)
            button.highlighted = False


def process_main_menu_click(window, mouseClickPos, grid):
    """Checks if any of the buttons in the window have been clicked on"""

    for button in window.mainButtons:
        if button.rect.collidepoint(mouseClickPos):

            # Checks if the start button has been pressed
            if button.text == "Start":

                # Changes the music
                pygame.mixer.stop()
                song = pygame.mixer.Sound("Data/Music/Girlfriendinacoma.wav")
                pygame.mixer.Sound.play(song, loops = -1)

                # Initialises the square_grid
                grid.initialise_square_grid(window.gameDisplay)
                # Initialises any blocks
                grid.initialise_blocks()
                # Adds the Exit
                grid.initialise_exit()
                # Adds the Spawner
                grid.initialise_spawner()
                # Initialises the dijk_grid
                grid.initialise_dijk_grid()
                # Initialises the route_dict
                grid.initialise_route_dict()

                grid.build_tower(1, "-", (3, 3))

                # Adds a Numemy
                grid.spawn_numemy(10, 10, 10, 1)
                grid.spawn_numemy(20, 10, 10, 2)
                grid.spawn_numemy(15, 10, 10, 3)

                Draw.draw_initial_in_game_window(window, grid)

                window.state = GameState.IN_GAME

            # Checks if the quit button has been pressed
            elif button.text == "Quit":
                pygame.event.post(pygame.event.Event(pygame.QUIT))


def process_in_game_click(window, mouseClickPos, grid):
    """Processes any left mouse clicks while in game"""
    for i, row in enumerate(grid.square_grid):
        for j, sqr in enumerate(row):
            if window.selectedEntity == None or not window.selectedEntity is sqr[0]:
                if (i, j) not in grid.forbidden_squares:
                    if sqr[0].surface.collidepoint(mouseClickPos):
                        squaresToDraw = []
                        if window.selectedEntity["square"] != None:
                            squaresToDraw.append(window.selectedEntity["position"])
                        window.selectedEntity = {"square" : sqr[0], "position" : (i, j)}
                        squaresToDraw.append(window.selectedEntity["position"])
                        Draw.draw_squares(window, grid, squaresToDraw)
                        return

    if window.selectedEntity["square"] != None:
        pos = window.selectedEntity["position"]
        if len(grid.square_grid[pos[0]][pos[1]]) > 1:
            tower = grid.square_grid[pos[0]][pos[1]][1]
            for button in window.sellButtons:
                if button.rect.collidepoint(mouseClickPos):
                    if button.text == 'Upgrade':
                        if tower.level >= 3:
                            # should print 'max level reached'
                            return
                        elif tower.level * tower.cost // 3 < grid.souls:
                            # should print 'not enough souls'
                            return
                        else:
                            grid.upgrade_tower(tower)
                            return
                    else:
                        grid.sell_tower(tower)
                        Draw.draw_squares(window, grid, [pos])
                        return
        # else:
        #     for button in window.buyButtons:
        #         if button.rect.collidepoint(mouseClickPos):
        #             if button.text == 'Buy':
        #                 if window.buyOperation == None:
        #                   # should print 'must choose an operation'  
        #                     return
        #                 if window.buyValue == None:
        #                   # should print 'must choose a value'
        #                     return
        #                 grid.build_tower(window.buyValue, window.buyOperation, 5, (pos[0], pos[1]))
        #                 window.buyOperation = None
        #                 window.buyValue = None
        #                 Draw.draw_squares(window, grid, [pos])
        #                 return
        #             elif button.text in ['+', '-', '*', '/']:
        #                 window.buyOperation = button.text
        #                 return  
        #             else:



                        