import threading
import Draw as Draw
import pygame
import ProcessInput as ProcessInput
from GameState import GameState
from Button import Button
from Numemy import Numemy
from Square import Exit


LEFT = 1
RIGHT = 3


class Window:
    """Deals with what is displayed on a window as well as any user inputs into that window"""

    def __init__(self, gameDisplay, width, height):
        self.gameDisplay = gameDisplay
        self.width = width
        self.height = height
        self.screenRatio = self.height / 1080
        self.mainButtons = []
        self.buyButtons = []
        self.sellButtons = []
        self.state = None
        self.selectedEntity = {"square" : None, "position" : None}
        self.buyValue = None
        self.buyOperation = None

    def change_state_to(self, newState):
        """Changes the state of the window object to the given state and draws the appropriate window"""
        self.state = newState
        if newState == GameState.MAIN_MENU:
            self.draw_main_menu()

    def create_main_menu(self):
        """Sets up the buttons of the main menu and draws them"""

        green = (0, 0, 0)
        screenWidth, screenHeight = self.gameDisplay.get_size()

        # Gets the size ratio between this screen and a 1920 * 1080 screen
        screenRatio = screenHeight / 1080

        # Creates the start game button of the main menu
        text = "Start"
        button1X = self.width / 10
        button1Y = self.height / 3
        fontSize = int(50 * screenRatio)
        font = Draw.create_font_object(text, fontSize, 7)
        width = font.get_width()
        height = font.get_height()
        rect = pygame.Rect(button1X, button1Y, width, height)

        startButton = Button(rect, font, green, text)


        # Creates the quit game button of the main menu
        text = "Quit"
        button2X = button1X
        button2Y = button1Y + height
        fontSize = int(50 * screenRatio)
        font = Draw.create_font_object(text, fontSize, 7)
        width = font.get_width()
        height = font.get_height()
        rect = pygame.Rect(button2X, button2Y, width, height)

        quitButton = Button(rect, font, green, text)

        self.mainButtons = [startButton, quitButton]
        Draw.draw_menu(self, self.mainButtons)
        Draw.draw_image(self.gameDisplay, "Numbers.jpg", self.width / 2, self.height / 3)

    def start_opening(self, lock):
        """Plays the intro then draws the main menu"""

        Draw.create_opening_animation(self, lock)
        if self.state == GameState.IN_OPENING_SCENE:
            self.state = GameState.MAIN_MENU
            self.create_main_menu()

    def start_opening_thread(self, lock):
        """Creates a thread that will run the opening sequence"""
        try:
            t = threading.Thread(target = self.start_opening, args=(lock, ))
            t.daemon = True # die when the main thread dies
            t.start()

        except Exception as e:
            print(e)

    def process_main_menu_event(self, event, grid):
        """Processes an event that occurred while the window is on the main menu"""

        # Checks if the mouse has hovered over any of the buttons on the main menu
        if event.type == pygame.MOUSEMOTION:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_menu_hover(self, mouseClickPos, self.mainButtons)
        
        # Checks if a mouse click has clicked on any of the main menu buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_main_menu_click(self, mouseClickPos, grid)

    def process_opening_scene_event(self, event, lock):
        """Processes any events that have occurred during the opening scene of Maths TD"""

        # If space has been pressed the opening scene is skipped
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = GameState.MAIN_MENU

            # Blocks until the opening animation thread releases the lock
            lock.acquire()
            lock.release()

            self.create_main_menu()

    def process_in_game_event(self, event, grid):
        """Processes an event that occurred while the window is in game"""

        # Checks if the mouse has hovered over any of the buttons on the side menu
        if event.type == pygame.MOUSEMOTION and self.selectedEntity["square"] != None:
            pos = self.selectedEntity["position"]
            if len(grid.square_grid[pos[0]][pos[1]]) > 1:
                mouseClickPos = pygame.mouse.get_pos()
                ProcessInput.process_menu_hover(self, mouseClickPos, self.sellButtons)
            else:
                mouseClickPos = pygame.mouse.get_pos()
                ProcessInput.process_menu_hover(self, mouseClickPos, self.buyButtons)


        # Checks if a mouse click has clicked on any of the squares or side menu buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_in_game_click(self, mouseClickPos, grid)

        elif event.type == pygame.KEYDOWN:
            key = event.key
            ProcessInput.process_in_game_key(self, key)


    def move_numemies(self, grid):
        """Moves the Numemies by one"""
        squaresToDraw = []
        new_num_loc_list = []
        movedNumemyFromSpawn = False
        exitSqr = grid.square_grid[grid.exit_square[0]][grid.exit_square[1]][1]
        for num_loc in grid.num_loc_list:
            for object in grid.square_grid[num_loc[0]][num_loc[1]]:
                if isinstance(object, Numemy):

                    # Only allows one numemy move out of the spawn at a time
                    if num_loc == grid.spawner_square:
                        if not movedNumemyFromSpawn:
                            movedNumemyFromSpawn = True
                        else:
                            new_num_loc_list.append(num_loc) # Re adds the numemy that waited for this round of movements
                            continue

                    squaresToDraw.append(num_loc)
                    grid.square_grid[num_loc[0]][num_loc[1]].remove(object)

                    # Checks if the numemy is at the exit, if it is then the numemy is removed else numemy is moved by 1
                    if object.next_square(grid) == grid.exit_square:

                        # When a numemy escapes the exits value is decreases by the numemies value
                        object.escape(grid)
                        exitSqr.value -= object.weight
                        if exitSqr.value < 0:
                            exitSqr.value = 0
                        squaresToDraw.append(grid.exit_square)
                    else:
                        object.location = object.next_square(grid)
                        new_num_loc_list.append(object.location)
                        squaresToDraw.append(object.location)
                        grid.square_grid[object.location[0]][object.location[1]].append(object)
        grid.num_loc_list = new_num_loc_list
        grid.update_forbidden_squares()
        Draw.draw_squares(self, grid, squaresToDraw)

        # Checks if the exit square value is 0, if it is then game is over
        if exitSqr.value == 0:
            self.state = GameState.GAME_OVER
            Draw.draw_game_over(self.gameDisplay, self.screenRatio)


    def shoot_towers(self, grid, counter, framerate):
        """Checks if any of the towers on the grid can shoot a numemy"""
        squaresToDraw = []
        for tower in grid.tower_list:
            if counter % (framerate / tower.speed) == 0:
                target = tower.find_targets(grid)
                if target is not None:
                    tower.attack(grid, target)
                    squaresToDraw.append(tower.location)
        Draw.draw_squares(self, grid, squaresToDraw)
