import threading
import Draw
import pygame
import ProcessInput
from GameState import GameState
from Button import Button


LEFT = 1
RIGHT = 3



class Window():
    """Deals with what is displayed on a window as well as any user inputs into that window"""

    def __init__(self, gameDisplay, width, height):
        self.gameDisplay = gameDisplay
        self.width = width
        self.height = height
        self.buttons = []
        self.state = None


    def change_state_to(self, newState):
        """Changes the state of the window object to the given state and draws the appropriate window"""
        self.state = newState
        if newState == GameState.MAIN_MENU:
            self.draw_main_menu()


    def create_main_menu(self):
        """Sets up the buttons of the main menu and draws them"""

        green = (0, 0, 0)

        # Creates the start game button of the main menu
        text = "Start"
        button1X = self.width / 10
        button1Y = self.height / 3
        font = Draw.create_font_object(text)
        width = font.get_width()
        height = font.get_height()
        rect = pygame.Rect(button1X, button1Y, width, height)

        startButton = Button(rect, font, green, text)


        # Creates the quit game button of the main menu
        text = "Quit"
        button2X = button1X
        button2Y = button1Y + height
        font = Draw.create_font_object(text)
        width = font.get_width()
        height = font.get_height()
        rect = pygame.Rect(button2X, button2Y, width, height)

        quitButton = Button(rect, font, green, text)

        self.buttons = [startButton, quitButton]
        Draw.draw_menu(self, self.buttons)


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
            print (e)



    def process_main_menu_event(self, event):
        """Processes an event that occurred while the window is on the main menu"""

        # Checks if the mouse has hovered over any of the buttons on the main menu
        if event.type == pygame.MOUSEMOTION:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_main_menu_hover(self, mouseClickPos)
        
        # Checks if a mouse click has clicked on any of the main menu buttons
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_main_menu_click(self, mouseClickPos)



    def process_opening_scene_event(self, event, lock):
        """Processes any events that have occurred during the opening scene of Maths TD"""

        # If space has been pressed the opening scene is skipped
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = GameState.MAIN_MENU

            # Blocks until the opening animation thread releases the lock
            lock.acquire()
            lock.release()

            self.create_main_menu()




        
        

