#import the modules
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import re
import operator
from pynput.keyboard import Controller, Key
from word2number import w2n
import psutil
import subprocess

#make the main variables

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

#the play audio function

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
            speak(f"Ok, my new name is {bot_name}. How can I help you, {user_name}?")

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

    # Handling unknown commands
    else:
        speak("Sorry, I don't understand that command.")

#the start of the application

print("Welcome to our App \n")
print("Let's setup settings \n")
user_name = input("Please Enter your name: ")

while True:
    bot_gender = input("please Chose the bot gender boy or girl(b/g): ")
    if bot_gender == "b":
        bot_name = "Anubise"
        engine.setProperty('voice', voices[0].id)
        break


    elif bot_gender == "g":
        bot_name = "bastet"
        engine.setProperty('voice', voices[1].id)
        
        break

    else:
        print("Invalid input. Please enter 'b' for boy or 'g' for girl.")

speak(f"Hello {user_name}! I'm your voice assistant.")
while True:
    command = listen()
    execute_command(command)