import speech_recognition as sr
import pyttsx3
import webbrowser
import openai
import os
import datetime
import wikipedia
import pyautogui

# OpenAI API Key (Replace with your own)
openai.api_key = None  # Set to your API key if available

# Initialize the TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Speed of speech
engine.setProperty("voice", engine.getProperty("voices")[1].id)  # Change voice

# Function to speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize voice
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        return "Sorry, I didn't understand that."
    except sr.RequestError:
        return "Request error. Check internet connection."

# Function to get response from OpenAI
def chat_with_gpt(prompt):
    if openai.api_key is None:
        return "OpenAI API key not set. Please provide your API key to use AI features."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error with OpenAI API: {str(e)}"

# Function to execute commands
def execute_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open microsoft edge" in command:
        speak("Opening microsoft edge")
        webbrowser.open("https://www.microsoft edge.com")
    
    elif "search wikipedia" in command:
        speak("What should I search?")
        query = listen()
        if query:
            speak(f"Searching Wikipedia for {query}")
            result = wikipedia.summary(query, sentences=2)
            speak(result)
    
    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")
    
    elif "date" in command:
        date_today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {date_today}")

    elif "screenshot" in command:
        speak("Taking a screenshot")
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        speak("Screenshot saved")

    elif "exit" in command or "stop" in command:
        speak("Goodbye!")
        exit()

    else:
        speak("Thinking...")
        response = chat_with_gpt(command)
        speak(response)

# Main loop
if __name__ == "__main__":
    speak("Hello, I am Jarvis. How can I assist you?")
    while True:
        user_command = listen()
        execute_command(user_command)
