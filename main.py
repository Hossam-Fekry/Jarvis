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

bot_name = None
user_name = None

keyboard = Controller()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

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



def calculate(expression):
    try:
        expression = re.sub(r'[^0-9+\-*/().]', '', expression)  # Remove unwanted characters
        result = eval(expression)
        return result
    except Exception as e:
        return None

def execute_command(command):
    global user_name, bot_name
    if command is None:
        return
    if "hello" in command:
        response = f"Hello {user_name}! How can I help you?"
        speak(response)
    elif "what is your name" in command or "what's your name" in command:
        response = f"My name is {bot_name}. How can I help you, {user_name}?"
        speak(response)
    elif "change your name" in command:
        speak("Ok, what is the new name?")
        new_name = listen()
        if new_name:
            bot_name = new_name
            speak(f"Ok, my new name is {bot_name}. How can I help you, {user_name}?")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The time is {now}"
        speak(response)
    elif "date" in command:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        speak(f"We are in year: {year}")
        speak(f"We are in month: {month}")
        speak(f"We are in day: {day}")
    elif "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad.exe")

    elif "open calculator" in command:
        speak("Opening Calculator")
        os.system("calc.exe")

    elif "search google for" in command:
        query = command.replace("search google for", "").strip()
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching Google for {query}")
        webbrowser.open(url)

    elif "empty recycle bin" in command:
        speak("Emptying the Recycle Bin")
        os.system("PowerShell.exe -Command Clear-RecycleBin -Confirm:$false")
    
    elif "open vscode" in command or "open visual studio code" in command or "open vs code" in command or "vscode" in command:
        speak("Opening Visual Studio Code")
        os.system("code")
    
    elif "open idea" in command:
        speak("Opening IntelliJ IDEA")
        os.system("start idea64")

    elif "increase volume by " in command:
        query = command.replace("increase volume by", "").strip()
        increase_volume(query = query)
    
    elif "exit" in command or "bye" in command:
        speak("Goodbye!")
        time.sleep(1)
        exit()
    
    elif any(op in command for op in ["+", "-", "*", "x", "/"]):
        expression = command.replace("x", "*")
        result = calculate(expression)
        if result is not None:
            speak(f"The answer is {result}")
        else:
            speak("Sorry, I couldn't calculate that.")
    
    else:
        speak("Sorry, I don't understand that command.")

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