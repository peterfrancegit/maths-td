import threading
import Draw


class Window():

    def __init__(self, gameDisplay, width, height):
        self.gameDisplay = gameDisplay
        self.width = width
        self.height = height
        self.state = None


    # Creates a thread that draws the opening scene
    def run_opening_animation_thread(self):
        try:
            t = threading.Thread(target = Draw.create_opening_animation, args=(self, ))
            t.daemon = True # die when the main thread dies
            t.start()
        except Exception as e:
            print (e)

