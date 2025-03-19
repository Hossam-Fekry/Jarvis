#import the modules
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import re
from pynput.keyboard import Controller, Key
from word2number import w2n
import psutil
import subprocess
import requests
import pyautogui
import google.generativeai as genai
import screen_brightness_control as sbc
import keyboard as k
import winreg

#set the main settings

bot_name = None
user_name = None
keyboard = Controller()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
quran_playlist = "https://open.spotify.com/playlist/2Zi4QNF4bDwRmT1P6WMYiD?si=907d9ebb00194422"
Motivational_songs_playlist = "https://open.spotify.com/playlist/2hV85bws0imGH4u1kAG6UU?si=d4b7fab8ecb74c46"
is_spotify_installed = None
Weather_API_KEY = "60162e39da2b217fa415f9e8328572d4"
Weather_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
screenshot_number = 1
genai.configure(api_key="AIzaSyAukxMyWGqLILd_uHVeiZER5559WColdWw")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

#make the functions

def speak(text):   #the function to make the assistant talk
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

#the function to listen to the user
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No voice detected. Listening again...")
            return None
        except sr.UnknownValueError:
            response = "Sorry, I couldn't understand."
            speak(response)
            return None
        except sr.RequestError:
            response = "There was an error with the speech recognition service."
            speak(response)
            return None

#the increase volume function

def increase_volume(query):
    try:
        query = w2n.word_to_num(query)  # Convert words to numbers
        query = int(query)  # Ensure it's an integer

        if query % 2 != 0:  # If the number is odd
            query -= 1  # Reduce it to the nearest even number
            speak(f"I can only increase volume in even steps I will increase it by {query}")

        actual_presses = query // 2  # Adjust for 2x volume increase per press

        speak(f"Increasing volume by {query}")

        for i in range(actual_presses):
            keyboard.press(Key.media_volume_up)
            time.sleep(0.1)
            keyboard.release(Key.media_volume_up)

    except ValueError:
        speak("Sorry, I couldn't understand the volume number.")

#the decrease volume function

def decrease_volume(query):
    try:
        query = w2n.word_to_num(query)  # Convert words to numbers
        query = int(query)  # Ensure it's an integer

        if query % 2 != 0:  # If the number is odd
            query -= 1  # Reduce it to the nearest even number
            speak(f"I can only decrease volume in even steps. Decreasing volume by {query}")

        actual_presses = query // 2  # Adjust for 2x volume decrease per press

        speak(f"Decreasing volume by {query}")

        for i in range(actual_presses):
            keyboard.press(Key.media_volume_down)
            time.sleep(0.1)
            keyboard.release(Key.media_volume_down)

    except ValueError:
        speak("Sorry, I couldn't understand the volume number.")

#the mute volume function

def mute_volume():
        keyboard.press(Key.media_volume_mute)
        time.sleep(0.1)
        keyboard.release(Key.media_volume_mute)
        print("Volume muted")

def unmute_volume():
        keyboard.press(Key.media_volume_mute)
        time.sleep(0.1)
        keyboard.release(Key.media_volume_mute)
        print("Volume unmuted")
        speak("Volume unmuted")

#the calculation function

def calculate(expression):
    try:
        expression = re.sub(r'[^0-9+\-*/().]', '', expression)  # Remove unwanted characters
        result = eval(expression)
        return result
    except Exception as e:
        return None

#the battery checker function

def check_battrey():
    battrey = psutil.sensors_battery()
    
    if battrey is None:
        speak("battrey information is not available")
        return
    
    battrey_level = battrey.percent
    plugged = battrey.power_plugged

    if plugged == True:
        charghing_status = "plugged in"
    else:
        charghing_status = "Not Pluggd in"

    speak(f"battrey level is : {battrey_level}%")
    speak(f"charging status : {charghing_status}")

#the play audio functions

def play_audio():
    speak("What audio do you want to listen to? Quran or motivational songs")
    while True:
        category = listen()
        if category is None:
            continue  # Ignore empty input and listen again

        category = category.strip().lower()

        if "quran" in category:
            play_playlist(quran_playlist, "spotify:playlist:2Zi4QNF4bDwRmT1P6WMYiD")
            break

        elif "motivational" in category:
            play_playlist(Motivational_songs_playlist, "spotify:playlist:2hV85bws0imGH4u1kAG6UU")
            break

        else:
            speak("Please choose one of the available options")

def play_playlist(web_url, spotify_uri):
    speak("Do you have Spotify installed on your computer? Please answer with yes or no.")

    while True:
        is_spotify_installed = listen()
        if is_spotify_installed is None:
            continue  # Ignore empty input and listen again

        is_spotify_installed = is_spotify_installed.strip().lower()

        if is_spotify_installed == "yes":
            speak("Opening Spotify application.")
            subprocess.Popen(["cmd", "/c", f"start {spotify_uri}"], shell=True)  # Opens in Spotify app
            break  # Ensure only one opens

        elif is_spotify_installed == "no":
            speak("Opening in web browser.")
            webbrowser.open(web_url)  # Opens in browser
            break  # Ensure only one opens

        else:
            speak("Please answer with yes or no.")

#the weather forcast function
def get_weather(city="Cairo"):
    try:
        params = {
            "q": city,
            "appid": Weather_API_KEY,
            "units": "metric",
            "lang": "en"
        }
        response = requests.get(Weather_BASE_URL, params=params)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"The weather in {city} is {description} with a temperature of {temp} degrees Celsius.")
        else:
            speak("Sorry, I couldn't fetch the weather data.")
    except Exception as e:
        speak("An error occurred while fetching the weather data.")

#the screenshot taking function
def take_screenshot():
    global screenshot_number
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    screenshot_path = os.path.join(desktop, f"screenshot{screenshot_number}.png")
    screensshot = pyautogui.screenshot()
    screensshot.save(screenshot_path)
    speak("Screenshot saved on your desktop.")
    screenshot_number += 1


#the check user_data_file function

def check_content_user_data_file(line,line_number):
    return line
#the assistant start function

def assistant_start():
    
    global user_name
    global bot_name

    print("Welcome to our App \n")
    
    #the start of the application
    if os.path.exists("user_data_file.txt"):
        with open("user_data_file.txt", "r") as file:
            first_line = file.readline().strip()
            second_line = file.readline().strip()
        
        user_name = check_content_user_data_file(first_line,1)
        bot_gender = check_content_user_data_file(second_line,2)

        if bot_gender == "b":
            bot_name = "Jarvis"
            engine.setProperty('voice', voices[0].id)

        elif bot_gender == "g":
            bot_name = "Luna"
            engine.setProperty('voice', voices[1].id)

    else:
        print("Let's setup settings \n")
        
        with open("user_data_file.txt", "w") as file:
            
            user_name = input("Please Enter your name: ")
            file.write(f"{user_name}\n")

            while True:
                bot_gender = input("please Chose the bot gender boy or girl(b/g): ")
                if bot_gender == "b":
                    bot_name = "Jarvis"
                    engine.setProperty('voice', voices[0].id)
                    file.write(f"{bot_gender}\n")
                    break


                elif bot_gender == "g":
                    bot_name = "Luna"
                    engine.setProperty('voice', voices[1].id)
                    
                    break

                else:
                    print("Invalid input. Please enter 'b' for boy or 'g' for girl.")

    speak(f"Hello {user_name}! I'm your voice assistant.")
    while True:
        command = listen()
        execute_command(command)

def get_default_browser_name():
    try:
        # Open registry key for HTTP protocol
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
            browser_prog_id, _ = winreg.QueryValueEx(key, "ProgId")

        # Mapping common ProgId values to actual browser names
        browser_map = {
            "ChromeHTML": "Chrome",
            "MSEdgeHTM": "Edge",
            "FirefoxURL": "Firefox",
            "OperaStable": "Opera",
            "BraveHTML": "Brave"
        }

        # Get browser name from mapping or return the raw ProgId if unknown
        return browser_map.get(browser_prog_id, browser_prog_id)
    
    except Exception:
        return "Unknown"

def close_program(program_name):
    """Find and terminate all processes matching the given program name."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process.info['name'].lower() == program_name.lower():
                print(f"Closing {program_name} (PID: {process.info['pid']})")
                process.kill()  # Forcefully terminate the process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


# The commands function
def execute_command(command):
    global user_name, bot_name
    if command is None:
        return

    # Greeting the user
    if "hello" in command:
        response = f"Hello {user_name}! How can I help you?"
        speak(response)

    # Responding to the assistant's name
    elif "what is your name" in command or "what's your name" in command:
        response = f"My name is {bot_name}. How can I help you, {user_name}?"
        speak(response)

    # Changing the assistant's name
    elif "change your name" in command:
        speak("Ok, what is the new name?")
        new_name = listen()
        if new_name:
            bot_name = new_name
            speak(f"Ok, my new name is {bot_name}, How can I help you, {user_name}?")

    # Telling the current time
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {now}"
        speak(response)

    # Telling the current date
    elif "date" in command:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        speak(f"We are in year: {year}")
        speak(f"We are in month: {month}")
        speak(f"We are in day: {day}")

    # Opening Notepad
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    # Opening Calculator
    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    # Searching Google
    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching Google for {query}")
        webbrowser.open(url)

    #Searching youtube
    elif "search youtube for" in command:
        query = command.replace("search youtube for", "").strip()
        url = f"https://www.youtube.com/results?search_query={query}"
        speak(f"Searching YouTube for {query}")
        webbrowser.open(url)


    # Emptying the Recycle Bin
    elif "empty recycle bin" in command:
        speak("Emptying the Recycle Bin")
        os.system("PowerShell.exe -Command Clear-RecycleBin -Confirm:$false")

    # Opening Visual Studio Code
    elif "open vscode" in command or "open visual studio code" in command or "open vs code" in command or "vscode" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

    # Opening IntelliJ IDEA
    elif "open idea" in command:
        speak("Opening IntelliJ IDEA")
        os.system("start idea64")

    # Increasing volume
    elif "increase volume by " in command:
        query = command.replace("increase volume by", "").strip()
        increase_volume(query=query)

    # Decreasing volume
    elif "decrease volume by" in command:
        query = command.replace("decrease volume by", "").strip()
        decrease_volume(query=query)

    # Muting the volume
    elif "mute" in command or "mute audio" in command or "mute volume" in command:
        mute_volume()

    # Unmuting the volume
    elif "unmute" in command or "unmute audio" in command or "unmute volume" in command:
        unmute_volume()

    # Checking battery status
    elif "battery" in command:
        check_battrey()

    #play an audio
    elif "play an audio" in command or "play audio" in command:
        play_audio()

    elif "pause" in command or "play" in command:
        keyboard.press_and_release("play/pause media")

    elif "next track" in command:
        keyboard.press_and_release("next track")

    elif "previous track" in command:
        keyboard.press_and_release("previous track")

    #get the weather in a city
    elif "weather" in command or "forecast" in command:
        speak("Which city's weather would you like to check?")
        city = listen()
        if city:
            get_weather(city)

    #take a screenshot
    elif "take a screenshot" in command or "screenshot" in command:
        take_screenshot()

    #set the brightness
    elif "set brightness to " in command:
        query = command.replace("set brightness to", "").strip()
        sbc.set_brightness(query)
        speak(f"Brightness set to {query}%")
    
    elif "open browser" in command or "open default browser" in command:
        browser_name = get_default_browser_name()
        os.startfile(f"{browser_name}.exe")

    elif "close browser" in command or "close default browser" in command:
        browser_name = f"{get_default_browser_name()}.exe"
        close_program(browser_name)


    #asking gemini
    elif "gemini" in command:
        speak("OK, say your question for gemini")
        gemini_c = listen()
        response = model.generate_content(gemini_c)
        speak("this answer is from gemini")
        speak(response.text)
        
    elif "type " in command:
        text = command.replace("type", "").strip()
        for char in text:
            k.write(char)
            time.sleep(0.05)
        k.write(" ")

    # Exiting the program
    elif "exit" in command or "bye" in command:
        speak("Goodbye!")
        time.sleep(1)
        exit()

    # Performing mathematical calculations
    elif any(op in command for op in ["+", "-", "*", "x", "/"]):
        expression = command.replace("x", "*")
        result = calculate(expression)
        if result is not None:
            speak(f"The answer is {result}")
        else:
            speak("Sorry, I couldn't calculate that.")

    # Handling unknown commands (get answers from gemini)
    else:
        speak("I'm sorry, I can't understand that command.")
        speak("do you want an answer from gemini")
        want_answer_from_gemini = listen()
        if want_answer_from_gemini == "yes":
            response = model.generate_content(command)
            speak("this answer is from gemini")
            speak(response.text)
        elif want_answer_from_gemini == "no":
            speak("ok I will not get an answer from gemini")

#the start of the application


assistant_start()
