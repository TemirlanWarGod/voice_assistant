import os
from win32com.client import Dispatch
import winreg
import shutil

def create_shortcut(target, shortcut_name, shortcut_folder):
    """Создание ярлыка для приложения"""
    shortcut_path = os.path.join(shortcut_folder, f"{shortcut_name}.lnk")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.save()
    print(f"Ярлык для {shortcut_name} создан в {shortcut_path}")

def find_apps_in_directory(directory):
    """Поиск .exe файлов в директории"""
    apps = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.exe'):
                apps.append(os.path.join(root, file))
    return apps

def find_installed_apps():
    """Автоматический поиск популярных приложений"""
    # Системные папки
    system_dirs = [
        r"C:\\Program Files",
        r"C:\\Program Files (x86)",
        os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
    ]
    
    apps = []
    
    # Поиск в системных директориях
    for directory in system_dirs:
        if os.path.exists(directory):
            apps.extend(find_apps_in_directory(directory))
    
    return apps

def main():
    # Папка для ярлыков на рабочем столе
    shortcut_folder = r"D:\\Projects\\venv\\Include\\Shortcuts"
    
    if not os.path.exists(shortcut_folder):
        os.makedirs(shortcut_folder)

   # Поиск установленных приложений
    print("Поиск приложений...")
    apps = find_installed_apps()

    # Создаем ярлыки для найденных приложений
    print("Создание ярлыков...")
    for app in apps:
        # Берем название приложения из пути к файлу (без расширения .exe)
        app_name = os.path.basename(app).replace(".exe", "")
        create_shortcut(app, app_name, shortcut_folder)

    print(f"Ярлыки для приложений созданы в {shortcut_folder}")

if __name__ == "__main__":
    main()