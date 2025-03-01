from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

def increase_volume():
    keyboard.press(Key.media_volume_up)
    time.sleep(0.1)
    keyboard.release(Key.media_volume_up)
    print("Volume increased")

for i in range(50):
    increase_volume()
