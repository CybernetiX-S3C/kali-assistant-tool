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
def load_commands():
    commands = []
    with open('kali_commands.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            command = {
                'command': row['command'],
                'description': row['description'],
                'type': row['type'],
                'ip': input(f"Enter the IP for {row['command']}: "),
                'port': input(f"Enter the port for {row['command']}: ")
            }
            commands.append(command)
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
commands = load_commands()

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
    url = "https://www.google.com/search?q=" + query
    webbrowser.open(url)

# Function to open a website
def open_website(url):
    webbrowser.open(url)

# Function to plot a simple graph
def plot_graph(x, y):
    plt.plot(x, y)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Graph")
    plt.show()

# Function to check the installed versions of various libraries and frameworks
def check_versions():
    versions = {
        'Python': tf.__version__,
        'NumPy': np.__version__,
        'Pandas': pd.__version__,
        'Matplotlib': matplotlib.__version__,
        'Scipy': scipy.__version__,
        'Scikit-learn': sklearn.__version__,
        'TensorFlow': tf.__version__,
        'PyTorch': torch.__version__,
        'Requests': requests.__version__,
        'BeautifulSoup': BeautifulSoup.__version__,
        'Flask': Flask.__version__
    }
    for name, version in versions.items():
        print(f"{name}: {version}")

# Function to install a package using apt-get
def install_package(package):
    result = execute_package_installation(package)
    if result:
        print(result)
    else:
        print(f"Package {package} installed successfully.")

# Function to execute a specific command
def execute_command(command):
    command_type = command['type']
    ip = command['ip']
    port = command['port']
    
    if command_type == 'system':
        result = execute_system_command(f"{command['command']} {ip} {port}")
        if result:
            print(result)
    elif command_type == 'package':
        install_package(command['command'])

# Main program loop
def main():
    while True:
        command = listen().lower()
        
        if 'time' in command:
            get_current_time()
        
        elif 'joke' in command:
            tell_joke()
        
        elif 'calculate' in command:
            expression = command.replace('calculate', '')
            calculate(expression)
        
        elif 'search' in command:
            query = command.replace('search', '')
            search_web(query)
        
        elif 'open' in command:
            url = command.replace('open', '')
            open_website(url)
        
        elif 'plot' in command:
            x = np.linspace(0, 10, 100)
            y = eval(command.replace('plot', ''))
            plot_graph(x, y)
        
        elif 'check versions' in command:
            check_versions()
        
        elif 'install' in command:
            package = command.replace('install', '')
            install_package(package)
        
        elif 'exit' in command:
            break
        
        else:
            found = False
            for cmd in commands:
                if cmd['command'] in command:
                    found = True
                    execute_command(cmd)
                    break
            if not found:
                print("Kali Assistant: Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
