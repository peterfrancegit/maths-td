import threading
import Draw

# Creates a thread that draws the opening scene
def run_opening_animation_thread(gameDisplay, width, height, sharedThreadVariable):
    try:
        t = threading.Thread(target = Draw.create_opening_animation, args=(gameDisplay, width, height, sharedThreadVariable))
        t.daemon = True # die when the main thread dies
        t.start()
    except Exception as e:
        print (e)