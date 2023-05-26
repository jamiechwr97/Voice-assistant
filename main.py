import speech_recognition as sr
import pyttsx3

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#for voice in voices:
   #engine.setProperty('voice', voice.id)
   #engine.say('What can I help you with sir?')
engine.runAndWait()
engine.setProperty('voice', voices[1].id)

engine.say('What can I help you with sir?')
engine.runAndWait()

try:
    with sr.Microphone() as source:
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if 'jarvis' in command:
            engine.say(command)
            engine.runAndWait()
            print(command)
        print(command)
except:
    pass