import psutil

def check_battery_status():
    battery = psutil.sensors_battery()
    
    if battery is None:
        print("Battery information is not available.")
        return
    
    percent = battery.percent
    plugged = battery.power_plugged

    # status = "Plugged in" if plugged else "Not plugged in"
    print(f"Battery Level: {percent}%")
    print(f"Charging Status: {plugged}")

check_battery_status()
