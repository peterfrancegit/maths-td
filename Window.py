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

        # Creates the start game button of the main menu
        button1X = self.width / 10
        button1Y = self.height / 3
        text = Draw.create_text_object("Start game")
        width = text.get_width()
        height = text.get_height()
        rect = pygame.Rect(button1X, button1Y, width, height)

        green = (0, 0, 0)
        button1 = Button(rect, text, green)
        self.buttons = [button1]
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

        if event.type == pygame.MOUSEMOTION:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_main_menu_hover(self, mouseClickPos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            mouseClickPos = pygame.mouse.get_pos()
            ProcessInput.process_main_menu_click(self, mouseClickPos)




        
        

