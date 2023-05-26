import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import python_weather

import asyncio
import os

opening_phrases = [
    {
        "name": "morning_phrases",
        "phrases": [
            "Good morning sir, what can I help you with?",
            "How may I assist you?",
            "Good day sir, how can I help you?"
        ]
    },
    {
        "name": "afternoon_phrases",
        "phrases": [
            "Good afternoon sir, what can I help you with?",
            "How may I assist you?",
            "Afternoon sir, how can I help you?"
        ]
    },
    {
        "name": "evening_phrases",
        "phrases": [
            "Good evening sir, what can I help you with?",
            "How may I assist you?",
            "Good evening sir, how can I help you?"
        ]
    },
    {
        "name": "night_phrases",
        "phrases": [
            "It's very late sir, what can I help you with?",
            "How may I assist you?",
            "You're up late sir, how can I help you?"
        ]
    },
]
repeat_phrases = [
    "can you repeat please, i didn't understand.",
    "i didn't hear you properly, can you repeat please?",
    "can you say that again?"
]
various_repeat_phrases = [
    "excuse me, but I still don't understand. May you please repeat?",
    "I'm still not to sure what you mean, can you say that again?"
]
anything_else_phrases = [
    "Can I help you with anything else sir?",
    "Do you need anything else?",
    "Anything else sir?"
]
repeat_question = False
opening_phrase_used = False
repeat_times = 0
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#for voice in voices:
   #engine.setProperty('voice', voice.id)
   #engine.say('What can I help you with sir?')
engine.runAndWait()
engine.setProperty('voice', voices[1].id)

def get_opening_phrase():
    global opening_phrase_used
    time = datetime.datetime.now()

    if (time.hour >= 6 and time.minute >= 00) and (time.hour <= 11 and time.minute <= 59):
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[0]["phrases"][pos])
    elif (time.hour <= 19 and time.minute <= 59) and (time.hour >= 12 and time.minute >= 00):
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[1]["phrases"][pos])
    elif (time.hour <= 23 and time.minute <= 59) and (time.hour >= 20 and time.minute >= 00):
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[2]["phrases"][pos])
    elif (time.hour <= 5 and time.minute <= 59) and (time.hour >= 0 and time.minute >= 00):
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[3]["phrases"][pos])

    opening_phrase_used = True

def get_anything_else(repeat):
    global repeat_times

    if repeat == False:
        pos = random.randint(0, 2)
        talk(anything_else_phrases[pos])
        repeat_times = 0
    elif repeat == True and repeat_times < 1:
        pos = random.randint(0, 2)
        talk(repeat_phrases[pos])
        repeat_times += 1
    elif repeat == True and repeat_times >= 1:
        pos = random.randint(0, 1)
        talk(various_repeat_phrases[pos])
        repeat_times += 1

async def getweather():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Villajoyosa')
        engine.say("Today's forecast is " + weather.current.temperature)

        talk('Would you like to know the forecast for the next few days?')
        command = take_command()

        if 'yes' in command:
            for forecast in weather.forecasts:
                talk(forecast)
                print(forecast)
        elif 'no' in command:
            talk('Okey')

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
                print(command)
    except:
        command = ''
    return command
def run_jarvis():
    global repeat_question
    global opening_phrase_used

    if opening_phrase_used == False:
        get_opening_phrase()
    elif opening_phrase_used == True:
        get_anything_else(repeat_question)
    command = take_command()

    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        repeat_question = False
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        print('The current time is ' + time)
        talk('The current time is ' + time)
        repeat_question = False
    elif 'who is' in command:
    # it will use wikipedia to search for info
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
        repeat_question = False
    elif 'joke' in command:
        talk(pyjokes.get_joke())
        repeat_question = False
    elif 'weather' or 'forecast' in command:
        asyncio.run(getweather())
        repeat_question = False
    elif 'thank you' or 'no' in command:
        if 'thank you' in command:
            talk('You are welcome.')
        elif 'no' in command:
            talk('Okey, let me know if you need anything else.')

        return False
    else:
        print('No command found')
        repeat_question = True

while True:
    run_jarvis()