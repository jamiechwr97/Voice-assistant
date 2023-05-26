import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random
import python_weather
import phrases

import asyncio
import os


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
        pos = random.randint(0, len(phrases.opening_phrases[0]["phrases"]))
        talk(phrases.opening_phrases[0]["phrases"][pos])
    elif (time.hour <= 19 and time.minute <= 59) and (time.hour >= 12 and time.minute >= 00):
        pos = random.randint(0, len(phrases.opening_phrases[0]["phrases"]))
        talk(phrases.opening_phrases[1]["phrases"][pos])
    elif (time.hour <= 23 and time.minute <= 59) and (time.hour >= 20 and time.minute >= 00):
        pos = random.randint(0, len(phrases.opening_phrases[0]["phrases"]))
        talk(phrases.opening_phrases[2]["phrases"][pos])
    elif (time.hour <= 5 and time.minute <= 59) and (time.hour >= 0 and time.minute >= 00):
        pos = random.randint(0, len(phrases.opening_phrases[0]["phrases"]))
        talk(phrases.opening_phrases[3]["phrases"][pos])

    opening_phrase_used = True

def get_anything_else(repeat):
    global repeat_times

    if repeat == False:
        pos = random.randint(0, 2)
        talk(phrases.anything_else_phrases[pos])
        repeat_times = 0
    elif repeat == True and repeat_times < 1:
        pos = random.randint(0, 2)
        talk(phrases.repeat_phrases[pos])
        repeat_times += 1
    elif repeat == True and repeat_times >= 1:
        pos = random.randint(0, 1)
        talk(phrases.various_repeat_phrases[pos])
        repeat_times += 1

async def getweather():
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # fetch a weather forecast from a city
        weather = await client.get('Villajoyosa')
        engine.say("Today's forecast is " + str(weather.current.temperature))

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
    elif 'weather' or 'forecast' in command:    #CHECK HOW TO GET THE ASYNC WORKING WITHOUT IT GOING INTO THIS CONDITION ON EVERY LOOP
        getweather()
        repeat_question = False
    elif 'thank you' or 'no' in command:
        if 'thank you' in command:
            talk('You are welcome.')
        elif 'no' in command:
            talk('Okey, let me know if you need anything else.')

        return False
    else:   #FIX ELSE CONDITION, IT IS LOOPING THROUGH get_anything_else BUT DOESN'T SAY IT DIDN'T HEAR ANYTHING
        print('No command found')
        repeat_question = True

while True:
    run_jarvis()