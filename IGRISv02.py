# Интеллектуальный Генератор Речевых Интерактивных Сценариев 
#                         "ИГРИС"
#                          v.02
#___________________________________________________________


import os
import psutil
import subprocess
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "ru")
    engine.say(text)
    engine.runAndWait()

def get_available_programs():
    """
    Возвращает словарь с именами приложений и их путями для запуска.
    """
    start_menu_path = os.path.join(os.environ["PROGRAMDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")

    programs = {}

    for path in [start_menu_path, desktop_path]:
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(".lnk"):  # Файлы ярлыков
                    program_name = os.path.splitext(file)[0].lower()
                    programs[program_name] = os.path.join(root, file)

    #print (programs)
    return programs

def recognize_command():
    """
    Распознаёт голосовую команду и возвращает текст.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю вашу команду...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Распознано: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь. Попробуйте снова.")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")
        except sr.WaitTimeoutError:
            print("Время ожидания истекло. Попробуйте снова.")
    return None

def open_application(apps, command):
    """
    Открывает приложение на основе команды, если оно найдено.
    """
    if "открой" in command:
        for app_name, app_path in apps.items():
            if app_name in command:
                speak(f"Открываю приложение: {app_name}")
                subprocess.Popen(['start', app_path], shell=True)
                return True
        print("Приложение не найдено. Попробуйте снова.")
        return False

def close_application(app_name):
    """
    Закрывает приложение по имени.
    """
    for process in psutil.process_iter(['name']):
        try:
            if app_name.lower() in process.info['name'].lower():
                print(f"Закрываю приложение: {process.info['name']}")
                process.terminate()
                process.terminate()
                speak(f"Приложение {app_name} закрыто.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Приложение '{app_name}' не найдено.")
    speak(f"Приложение {app_name} не найдено.")
    return False

if __name__ == "__main__":
    print("Ищу доступные приложения...")
    available_programs = get_available_programs()

    print("Голосовой помощник готов. Скажите название приложения для запуска или 'выход' для завершения.")
    while True:
        command = recognize_command()
        if command:
            if "выход" in command:
                speak("Завершение работы.")
                break
            elif "игрис" in command:
                if "привет" in command or "я вернулся" in command or "работаем" in command:
                    speak("готов к работе")
                elif "открой" in command:
                    open_application(available_programs, command)
                elif "закрой" in command:
                    app_name = command.replace("игрис закрой", "").strip()
                    close_application(app_name)
            else:
                print("Команда не распознана. Скажите 'открой <имя>' или 'закрой <имя>'.")


#import speech_recognition as sr
#import pyttsx3
#import pyaudio 
#import subprocess
#import psutil
#import os
#
#
#def speak(text):
#    engine = pyttsx3.init()
#    engine.setProperty("rate", 150)
#    engine.setProperty("voice", "ru")
#    engine.say(text)
#    engine.runAndWait()
#
#print("1")
#
#def get_available_programs():
#    """
#    Возвращает словарь с именами приложений и их путями для запуска.
#    """
#    start_menu_path = os.path.join(os.environ["PROGRAMDATA"], "Microsoft", "Windows", "Start Menu", "Programs")
#    desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
#    
#    programs = {}
#
#    for path in [start_menu_path, desktop_path]:
#        for root, dirs, files in os.walk(path):
#            for file in files:
#                if file.endswith(".lnk"):  # Файлы ярлыков
#                    program_name = os.path.splitext(file)[0].lower()
#                    programs[program_name] = os.path.join(root, file)
#
#    return programs
#
#def recognize_command():
#    """
#    Распознаёт голосовую команду и возвращает текст.
#    """
#    recognizer = sr.Recognizer()
#    with sr.Microphone() as source:
#        print ("Слушаю")
#        try:
#            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#            command = recognizer.recognize_google(audio, language="ru-RU")
#            print(f"Распознано: {command}")
#            return command.lower()
#        except sr.UnknownValueError:
#            print("Не удалось распознать речь. Попробуйте снова.")
#        except sr.RequestError as e:
#            print(f"Ошибка сервиса распознавания: {e}")
#        except sr.WaitTimeoutError:
#            print("Время ожидания истекло. Попробуйте снова.")
#    return None
#
#def open_application(apps, command):
#    """
#    Открывает приложение на основе команды, если оно найдено.
#    """
#    if "игрис" in command:
#        if "привет" in command or "я вернулся" in command or "работаем" in command:
#            speak("готов к работе")
#        elif "открой" in command:
#            for app_name, app_path in apps.items():
#                if app_name in command:
#                    speak(f"Открываю приложение: {app_name}")
#                    subprocess.Popen(['start', app_path], shell=True)
#                    return True
#            print("Приложение не найдено. Попробуйте снова.")
#            return False
#        elif "закрой" in command:
#            """
#    Закрывает приложение по имени.
#    """
#    for process in psutil.process_iter(['name']):
#        try:
#            if app_name.lower() in process.info['name'].lower():
#                print(f"Закрываю приложение: {process.info['name']}")
#                process.terminate()
#                return True
#        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#            pass
#    print(f"Приложение '{app_name}' не найдено.")
#    return False
#
#if __name__ == "__main__":
#    print("Ищу доступные приложения...")
#    available_programs = get_available_programs()
#    
#    print("Голосовой помощник готов. Скажите название приложения для запуска или 'выход' для завершения.")
#    while True:
#        command = recognize_command()
#        if command:
#            if "выход" in command:
#                speak("Завершение работы.")
#                break
#            open_application(available_programs, command)
#            app_name = command.strip()
#            open_application(app_name)


#def recognize_speech():
#    recognizer = sr.Recognizer()
#    with sr.Microphone() as source:
#        print("Слушаю...")
#        audio = recognizer.listen(source)
#
#    try:
#        text = recognizer.recognize_google(audio, language= "ru-RU")
#        print(f"Я услышал: {text}")
#        return text
#    except sr.UnknownValueError:
#        print ("Непонял")
#    except sr.RequestError as e:
#        print(f"Ошибка сервиса: {e}")
#print("2")
#
#def speak(text):
#    engine = pyttsx3.init()
#    engine.setProperty("rate", 150)
#    engine.setProperty("voice", "ru")
#    engine.say(text)
#    engine.runAndWait()
#print("3")
#
#
#def assistant_logic(command):
#    if "открыть" in command:
#        # Здесь добавьте список приложений, которые могут быть открыты
#        if "Photoshop" in command:
#            speak("Открываю Photoshop.")
#            subprocess.Popen(["D:\Adobe\Adobe Photoshop 2020\\Photoshop.exe"])  # Открывает Photoshop
#        elif "браузер" in command:
#            speak("Открываю браузер.")
#            subprocess.Popen(["C:\\Users\\TemirLINE\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"])  # Открывает Google Chrome
#        elif "Steam" in command:
#            speak("Открываю Steam")
#            subprocess.Popen(["D:\\Downloads\\Steam\\steam.exe"]) # Открывает Steam
#        else:
#            speak("Неизвестная команда для открытия приложения.")
#        print("4")
#    else:
#        command = command.lower()
#        if 'привет' in command or 'начать работу' in command or 'поработаем' in command:
#            speak("Проверка пройдена")
#        elif "сколько время" in command:
#            from datetime import datetime
#            now = datetime.now().strftime("%H:%M")
#            speak(f"Сейчас {now}")
#        elif 'пока' in command or 'завершить работу' in command or 'закончили' in command:
#            speak("До встречи!")
#            exit()
#        else:
#            speak("Непонятная команда")
#
#def main():
#    while True:
#        command = recognize_speech()
#        if command:
#            assistant_logic(command)
#print("5")
#
#if __name__ == "__main__":
#    main()