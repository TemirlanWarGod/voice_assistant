import speech_recognition as sr
import pyttsx3
import pyaudio 
import subprocess
import os


print("1")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language= "ru-RU")
        print(f"Я услышал: {text}")
        return text
    except sr.UnknownValueError:
        print ("Непонял")
    except sr.RequestError as e:
        print(f"Ошибка сервиса: {e}")
print("2")

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "ru")
    engine.say(text)
    engine.runAndWait()
print("3")


def assistant_logic(command):
    if "открыть" in command:
        # Здесь добавьте список приложений, которые могут быть открыты
        if "Photoshop" in command:
            speak("Открываю Photoshop.")
            subprocess.Popen(["D:\Adobe\Adobe Photoshop 2020\\Photoshop.exe"])  # Открывает Photoshop
        elif "браузер" in command:
            speak("Открываю браузер.")
            subprocess.Popen(["C:\\Users\\TemirLINE\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"])  # Открывает Google Chrome
        elif "Steam" in command:
            speak("Открываю Steam")
            subprocess.Popen(["D:\\Downloads\\Steam\\steam.exe"]) # Открывает Steam
        else:
            speak("Неизвестная команда для открытия приложения.")
        print("4")
    else:
        command = command.lower()
        if 'привет' in command or 'начать работу' in command or 'поработаем' in command:
            speak("Проверка пройдена")
        elif "сколько время" in command:
            from datetime import datetime
            now = datetime.now().strftime("%H:%M")
            speak(f"Сейчас {now}")
        elif 'пока' in command or 'завершить работу' in command or 'закончили' in command:
            speak("До встречи!")
            exit()
        else:
            speak("Непонятная команда")

def main():
    while True:
        command = recognize_speech()
        if command:
            assistant_logic(command)
print("5")

if __name__ == "__main__":
    main()