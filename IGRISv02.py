# Интеллектуальный Генератор Речевых Интерактивных Сценариев 
#                         "ИГРИС"
#                          v.02
#___________________________________________________________


import os
import psutil
import subprocess
import speech_recognition as sr
import pyttsx3
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("voice", "ru")
    engine.say(text)
    engine.runAndWait()

# Поиск приложений
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

# Обработка голоса
def recognize_command():
    """
    Распознаёт голосовую команду и возвращает текст.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю вашу команду...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=30)
            command = recognizer.recognize_google(audio, language="ru-RU")
            if "игры" in command:
                command = command.replace("игры", "игрис").strip()
            elif "Игорь" in command:
                command = command.replace("Игорь", "игрис").strip()

            print(f"Распознано: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь. Попробуйте снова.")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания: {e}")
        except sr.WaitTimeoutError:
            print("Время ожидания истекло. Попробуйте снова.")
    return None

# Открывает приложение
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

# Закрывает приложение
def close_application(app_name):
    """
    Закрывает приложение по имени.
    """
    for process in psutil.process_iter(['name']):
        try:
            if app_name.lower() in process.info['name'].lower():
                print(f"Закрываю приложение: {process.info['name']}")
                process.terminate()
                speak(f"Приложение {app_name} закрыто.")
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    print(f"Приложение '{app_name}' не найдено.")
    speak(f"Приложение {app_name} не найдено.")
    return False


def open_links():
    if "YouTube" in command:
        speak("Открываю YouTube. Приятного просмотра")
        youtube_url = "https://www.youtube.com"
        webbrowser.open(youtube_url)
        return True
    elif "Telegram" in command:
        speak("Открываю Telegram. Желаю продуктивной работы")
        telegram_url = "https://web.telegram.org/"
        webbrowser.open(telegram_url)
        return True
    elif "WhatsApp" in command:
        speak("Открываю WhatsApp. Ждем собиседников")
        whatsapp_url= "https://web.whatsapp.com/"
        webbrowser.open(whatsapp_url)
        return True
    elif "GitHub" in command:
        speak("Открываю GitHub. Ждем обновлений для бота")
        github_url = "https://github.com/"
        webbrowser.open(github_url)
        return True
    else:
        speak("Ссылка не найдена. Введите в ручную")
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
                    if "ссылка" in command or "ссылку" in command:
                        open_links()
                    else:
                        open_application(available_programs, command)
                elif "закрой" in command:
                    app_name = command.replace("игрис закрой", "").strip()
                    close_application(app_name)
            else:
                print("Команда не распознана. Скажите 'открой <имя>' или 'закрой <имя>'.")

