import os
import shutil
import subprocess
from enum import Enum
from colorama import init, Fore

init(autoreset=True)

# Константы для путей и пакетов
CONFIG_PATHS = [
    "~/.config/bspwm",
    "~/.config/sxhkd",
    "~/.config/polybar",
    "~/.config/wallpapers",
]
PACKAGES = ["bspwm", "sxhkd", "dmenu", "feh", "picom", "polybar"]
BIN_SCRIPT = "~/bin/random_wallpaper.sh"
XINITRC = "~/.xinitrc"


class MenuChoice(Enum):
    INSTALL = "1"
    DELETE = "2"
    EXIT = "3"


# --- Утилиты ---
def run_command(command):
    """Выполняет shell-команду с проверкой ошибок."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Ошибка при выполнении команды '{command}': {e}")
        exit(1)


def safe_remove(path):
    """Безопасно удаляет файл или директорию."""
    expanded_path = os.path.expanduser(path)
    if os.path.exists(expanded_path):
        if os.path.isdir(expanded_path):
            shutil.rmtree(expanded_path)
        else:
            os.remove(expanded_path)
        print(Fore.YELLOW + f"Удалено: {expanded_path}")
    else:
        print(Fore.CYAN + f"Не найдено: {expanded_path}")


# --- Интерфейс ---
def print_ascii():
    print(Fore.RED + """
            ┌┬┐┌─┐┬─┐┬┌─┌┐┌┌─┐┌─┐┌─┐
             ││├─┤├┬┘├┴┐│││├┤ └─┐└─┐
            ─┴┘┴ ┴┴└─┴ ┴┘└┘└─┘└─┘└─┘
                    ♡𝔡3𝔯𝔯𝔨1𝔞♡
          vers 1.3
    """)


def print_help():
    print(Fore.RED + "         ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
    print(Fore.RED + "        │ " + Fore.CYAN + "[1]" + Fore.RESET + " Начать Установку" + Fore.RED + "          │")
    print(Fore.RED + "        │ " + Fore.CYAN + "[2]" + Fore.RESET + " Удалить прошлые конфиги" + Fore.RED + "   │")
    print(Fore.RED + "        │ " + Fore.CYAN + "[3]" + Fore.RESET + " Выход" + Fore.RED + "                     │")
    print(Fore.RED + "         ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺")
    print("")


# --- Установка ---
def install():
    run_command("sudo pacman -Syu --noconfirm")
    run_command(f"sudo pacman -S --noconfirm {' '.join(PACKAGES)}")

    home_config_dir = os.path.expanduser("~/.config")
    # Копирование конфигураций
    for config in ["bspwm", "sxhkd", "polybar"]:
        src = os.path.join("..", "src", config)
        dest = os.path.join(home_config_dir, config)
        shutil.copytree(src, dest, dirs_exist_ok=True)
        print(Fore.GREEN + f"Скопирован: {dest}")

    # Копирование обоев
    wallpapers_src = os.path.join("..", "src", "wallpapers")
    wallpapers_dest = os.path.join(home_config_dir, "wallpapers")
    shutil.copytree(wallpapers_src, wallpapers_dest, dirs_exist_ok=True)
    print(Fore.GREEN + f"Скопированы обои: {wallpapers_dest}")

    # Копирование скрипта
    bin_dir = os.path.expanduser("~/bin")
    os.makedirs(bin_dir, exist_ok=True)
    shutil.copy(os.path.join("..", "src", "script", "random_wallpaper.sh"), BIN_SCRIPT)
    os.chmod(BIN_SCRIPT, 0o755)
    print(Fore.GREEN + f"Скрипт установлен: {BIN_SCRIPT}")

    # Установка fish
    run_command("curl -L https://get.oh-my.fish | fish")
    run_command("omf install bobthefish")


# --- Удаление ---
def delete():
    for config in CONFIG_PATHS:
        safe_remove(config)
    safe_remove(XINITRC)
    safe_remove(BIN_SCRIPT)
    run_command(f"sudo pacman -Rns --noconfirm {' '.join(PACKAGES)}")
    print(Fore.GREEN + "Удаление завершено.")


# --- Главная функция ---
if __name__ == "__main__":
    run_command("clear")
    print_ascii()
    print_help()

    choice = input("*: ").strip()
    if choice == MenuChoice.INSTALL.value:
        install()
    elif choice == MenuChoice.DELETE.value:
        delete()
    elif choice == MenuChoice.EXIT.value:
        print(Fore.GREEN + "Выход.")
        exit(0)
    else:
        print(Fore.RED + "Неверный выбор.")
