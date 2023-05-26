import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import random

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
repeat_question = False
repeat_times = 0
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#for voice in voices:
   #engine.setProperty('voice', voice.id)
   #engine.say('What can I help you with sir?')
engine.runAndWait()
engine.setProperty('voice', voices[1].id)

def get_opening_phrase(repeat):
    global repeat_times
    time = datetime.datetime.now()

    if (time.hour >= 6 and time.minute >= 00) and (time.hour <= 11 and time.minute <= 59) and repeat != True:
        if repeat_times > 0:
            repeat_times = 0
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[0]["phrases"][pos])
    elif (time.hour <= 19 and time.minute <= 59) and (time.hour >= 12 and time.minute >= 00) and repeat != True:
        if repeat_times > 0:
            repeat_times = 0
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[1]["phrases"][pos])
    elif (time.hour <= 23 and time.minute <= 59) and (time.hour >= 20 and time.minute >= 00) and repeat != True:
        if repeat_times > 0:
            repeat_times = 0
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[2]["phrases"][pos])
    elif (time.hour <= 5 and time.minute <= 59) and (time.hour >= 0 and time.minute >= 00) and repeat != True:
        if repeat_times > 0:
            repeat_times = 0
        pos = random.randint(0, len(opening_phrases[0]["phrases"]))
        talk(opening_phrases[3]["phrases"][pos])
    elif repeat == True and repeat_times < 1:
        pos = random.randint(0, 2)
        talk(repeat_phrases[pos])
        repeat_times += 1
    elif repeat == True and repeat_times >= 1:
        pos = random.randint(0, 1)
        talk(various_repeat_phrases[pos])
        repeat_times += 1

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
    get_opening_phrase(repeat_question)
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
    elif 'thank you' in command:
        engine.say('You are welcome.')
        return False
    else:
        print('No command found')
        repeat_question = True

while True:
    run_jarvis()