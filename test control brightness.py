import screen_brightness_control as sbc

# Get current brightness
current_brightness = sbc.get_brightness()
print(f"Current Brightness: {current_brightness}%")

# Set brightness to 50%
sbc.set_brightness(100)
print("Brightness set to 50%")
