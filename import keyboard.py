import keyboard
import threading
import time

running = True

def press_e_repeatedly():
    while running:
        keyboard.press_and_release('e')
        time.sleep(0.1) 

thread = threading.Thread(target=press_e_repeatedly)
thread.start()

keyboard.wait('z')
running = False
thread.join()
print("Program oprit.")
