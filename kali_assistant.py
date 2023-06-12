import csv
import subprocess
import pyttsx3
import speech_recognition as sr
import datetime
import random
import webbrowser
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model
import tensorflow as tf
import torch
import requests
from bs4 import BeautifulSoup
from flask import Flask
import csv

# Load the commands from the CSV file
def load_commands(file_path):
    commands = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            commands.append(row)
    return commands

# Function to execute system commands
def execute_system_command(command):
    try:
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if output:
            return output.decode('utf-8')
        elif error:
            return error.decode('utf-8')
        else:
            return None
    except Exception as e:
        return f"Error executing system command: {str(e)}"

# Function to execute package installation command
def execute_package_installation(package):
    result = execute_system_command(f"apt-get install -y {package}")
    return result

# Load the commands from the CSV file
csv_file = 'kali_commands.csv'
commands = load_commands(csv_file)

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to listen to user's voice input
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("User: " + text)
            return text
        except sr.UnknownValueError:
            print("Kali Assistant: Sorry, I didn't understand that.")
        except sr.RequestError as e:
            print("Kali Assistant: Sorry, I'm unable to process your request at the moment.")
            print(f"Error: {str(e)}")
    return ""

# Function to speak the assistant's response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is " + current_time)

# Function to generate a random joke
def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I'm reading a book about anti-gravity. It's impossible to put down!",
        "Why don't skeletons fight each other? They don't have the guts!",
        "Did you hear about the mathematician who's afraid of negative numbers? He will stop at nothing to avoid them!",
        "I used to be a baker, but I couldn't make enough dough.",
    ]
    joke = random.choice(jokes)
    speak(joke)

# Function to perform basic arithmetic calculations
def calculate(expression):
    try:
        result = eval(expression)
        speak("The result is " + str(result))
    except Exception:
        speak("Sorry, I couldn't perform the calculation.")

# Function to search the web using a given query
def search_web(query):
    url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(url)
    speak("Here are the search results for " + query)

# Function to open a specific application or file
def open_application(application):
    if "browser" in application:
        speak("Opening the browser.")
        webbrowser.open("https://www.google.com")
    elif "text editor" in application:
        speak("Opening a text editor.")
        os.system("notepad")
    elif "calculator" in application:
        speak("Opening the calculator.")
        os.system("calc")
    else:
        speak("Sorry, I couldn't find the specified application.")

# Welcome message
speak("Welcome to Kali Assistant!")
speak("How can I assist you?")

# Start the virtual assistant loop
while True:
    user_input = listen()

    # Check if the user wants to exit
    if "exit" in user_input:
        speak("Goodbye!")
        break

    # Execute the command
    for command in commands:
        if user_input.lower() == command['command'].lower():
            if command['type'].lower() == 'system':
                result = execute_system_command(command['command'])
            elif command['type'].lower() == 'package':
                result = execute_package_installation(command['command'])
            else:
                result = "Command type not supported."

            # Provide response based on command execution
            if result:
                speak(result)
            else:
                speak("Command executed successfully.")
            break
    else:
        if "what's the time" in user_input:
            get_current_time()
        elif "tell me a joke" in user_input:
            tell_joke()
        elif "calculate" in user_input:
            expression = user_input.replace("calculate", "").strip()
            calculate(expression)
        elif "search" in user_input:
            query = user_input.replace("search", "").strip()
            search_web(query)
        elif "open" in user_input:
            application = user_input.replace("open", "").strip()
            open_application(application)
        else:
            speak("Sorry, I didn't understand that. Can you please repeat?")
