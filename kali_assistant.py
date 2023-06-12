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
import scipy
import sklearn
import tensorflow as tf
import torch
import requests
from bs4 import BeautifulSoup
from flask import Flask

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

# Function for numpy computations
def perform_numpy_computations():
    # Numpy computations here
    result = "Performed numpy computations."
    return result

# Function for pandas operations
def perform_pandas_operations():
    # Pandas operations here
    result = "Performed pandas operations."
    return result

# Function for matplotlib plotting
def perform_matplotlib_plotting():
    # Matplotlib plotting here
    result = "Performed matplotlib plotting."
    return result

# Function for scipy calculations
def perform_scipy_calculations():
    # Scipy calculations here
    result = "Performed scipy calculations."
    return result

# Function for scikit-learn machine learning
def perform_scikit_learn_machine_learning():
    # Scikit-learn machine learning here
    result = "Performed scikit-learn machine learning."
    return result

# Function for tensorflow deep learning
def perform_tensorflow_deep_learning():
    # TensorFlow deep learning here
    result = "Performed TensorFlow deep learning."
    return result

# Function for PyTorch deep learning
def perform_pytorch_deep_learning():
    # PyTorch deep learning here
    result = "Performed PyTorch deep learning."
    return result

# Function for sending HTTP requests
def send_http_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        result = "HTTP request sent successfully."
    else:
        result = "Failed to send HTTP request."
    return result

# Function for HTML parsing
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Perform HTML parsing operations here
    result = "Performed HTML parsing."
    return result

# Function for creating a Flask app
def create_flask_app():
    app = Flask(__name__)
    # Flask app creation code here
    result = "Created Flask app."
    return result

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
            elif command['type'].lower() == 'numpy':
                result = perform_numpy_computations()
            elif command['type'].lower() == 'pandas':
                result = perform_pandas_operations()
            elif command['type'].lower() == 'matplotlib':
                result = perform_matplotlib_plotting()
            elif command['type'].lower() == 'scipy':
                result = perform_scipy_calculations()
            elif command['type'].lower() == 'scikit-learn':
                result = perform_scikit_learn_machine_learning()
            elif command['type'].lower() == 'tensorflow':
                result = perform_tensorflow_deep_learning()
            elif command['type'].lower() == 'torch':
                result = perform_pytorch_deep_learning()
            elif command['type'].lower() == 'http':
                result = send_http_request(command['command'])
            elif command['type'].lower() == 'html':
                result = parse_html(command['command'])
            elif command['type'].lower() == 'flask':
                result = create_flask_app()
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

