import pygetwindow as gw
import pyautogui
import time

# Get the currently active window
active_window = gw.getActiveWindow()

if active_window:
    print(f"Active window: {active_window.title}")
    pyautogui.hotkey('alt', 'f4')
else:
    print("No active window found.")
