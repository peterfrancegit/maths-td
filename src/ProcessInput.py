import Draw as Draw
import pygame
from Button import Button
from Square import Square
from GameState import GameState
from Tower import tower_cost


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

    if isinstance(window.selectedEntity["square"], Square):
        pos = window.selectedEntity["position"]
        if len(grid.square_grid[pos[0]][pos[1]]) > 1:
            tower = grid.square_grid[pos[0]][pos[1]][1]
            for button in window.sellButtons:
                if button.rect.collidepoint(mouseClickPos):
                    if button.text == 'Upgrade':
                        if tower.level >= 3:
                            process_message_event(window, "Tower is already level 3")
                            return
                        elif tower.upgrade_cost > grid.souls:
                            process_message_event(window, "Not enough souls")
                            return
                        else:
                            tower.upgrade(grid)
                            process_soul_change(window, grid)
                            Draw.draw_squares(window, grid, [pos])
                            return
                    else:
                        grid.sell_tower(tower)
                        process_soul_change(window, grid)
                        Draw.draw_squares(window, grid, [pos])
                        return
        else:
            for button in window.buyButtons:
                if button.rect.collidepoint(mouseClickPos):
                    if button.text == 'Buy':
                        if window.buyOperation == None:
                            process_message_event(window, "Must choose operation for Tower")  
                            return
                        if window.buyValue == None:
                            process_message_event(window, "Must set value for Tower")
                            return
                        if grid.souls < tower_cost(window.buyValue, window.buyOperation):
                            process_message_event(window, "Not enough souls")
                            return
                        grid.build_tower(window.buyValue, window.buyOperation, (pos[0], pos[1]))
                        process_soul_change(window, grid)
                        window.buyOperation = None
                        window.buyValue = None
                        fontSize = Draw.get_fitted_size("", window.input.rect.width, window.input.rect.height)
                        font = Draw.create_font_object("", fontSize, 7)
                        window.input = Button(window.input.rect, font, (0, 0, 0), "")
                        Draw.draw_squares(window, grid, [pos])
                        Draw.draw_button(window, window.input)
                        return
                    else:
                        window.buyOperation = button.text
                        return  

def process_in_game_key(window, key):
    text = window.input.text
    if key == pygame.K_0:
        text += '0'
    elif key == pygame.K_1:
        text += '1'
    elif key == pygame.K_2:
        text += '2'
    elif key == pygame.K_3:
        text += '3'
    elif key == pygame.K_4:
        text += '4'
    elif key == pygame.K_5:
        text += '5'
    elif key == pygame.K_6:
        text += '6'
    elif key == pygame.K_7:
        text += '7'
    elif key == pygame.K_8:
        text += '8'
    elif key == pygame.K_9:
        text += '9'
    elif key == pygame.K_BACKSPACE:
        if len(text) > 0:
            text = text[:-1]
    else:
        return
    if len(text) == 0:
        window.buyValue = None
    else:
        window.buyValue = int(text)
    fontSize = Draw.get_fitted_size(text, window.input.rect.width, window.input.rect.height)
    font = Draw.create_font_object(text, fontSize, 7)
    window.input = Button(window.input.rect, font, (0, 0, 0), text)
    Draw.draw_button(window, window.input)

def process_message_event(window, message):
    fontSize = Draw.get_fitted_size(message, window.message_box.rect.width, window.message_box.rect.height)
    font = Draw.create_font_object(message, fontSize, 8)
    window.message_box = Button(window.message_box.rect, font, (100, 100, 100), message)
    Draw.draw_button(window, window.message_box)

def process_soul_change(window, grid):
    text = "Souls: " + str(grid.souls)
    fontSize = Draw.get_fitted_size(text, window.souls_box.rect.width, window.souls_box.rect.height)
    font = Draw.create_font_object(text, fontSize, 7)
    window.souls_box = Button(window.souls_box.rect, font, (100, 100, 100), text)
    Draw.draw_button(window, window.souls_box)
                        