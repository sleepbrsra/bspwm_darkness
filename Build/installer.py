import os
import shutil
import subprocess
from colorama import init, Fore

init(autoreset=True)

def print_ascii():
    print(Fore.RED + """
            ┌┬┐┌─┐┬─┐┬┌─┌┐┌┌─┐┌─┐┌─┐
             ││├─┤├┬┘├┴┐│││├┤ └─┐└─┐
            ─┴┘┴ ┴┴└─┴ ┴┘└┘└─┘└─┘└─┘
                    ♡𝔡3𝔯𝔯𝔨1𝔞♡
          vers 1.3
    """)

def print_help():
    print(Fore.RED + "         ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯")
    print(Fore.RED + "        │ " + Fore.CYAN + "[1]" + Fore.RESET + " Начать Установку" + Fore.RED + "          │")
    print(Fore.RED + "        │ " + Fore.CYAN + "[2]" + Fore.RESET + " Удалить прошлые конфиги" + Fore.RED + "   │")
    print(Fore.RED + "        │ " + Fore.CYAN + "[3]" + Fore.RESET + " Выход" + Fore.RED + "                     │")
    print(Fore.RED + "         ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺")
    print("")

# -------------------
def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команды '{command}': {e}")
        exit(1)

def copy_configs(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)  # Удаляем старую директорию, если она существует
    shutil.copytree(src, dest)  # Копируем новую конфигурацию
# -----------------


def main():
    run_command("sudo pacman -Syu --noconfirm")
    run_command("sudo pacman -S --noconfirm bspwm sxhkd dmenu feh picom polybar")

    # Копирование конфигураций
    home_config_dir = os.path.expanduser("~/.config")
    copy_configs(os.path.join("..", "src", "bspwm"), os.path.join(home_config_dir, "bspwm"))
    copy_configs(os.path.join("..", "src", "sxhkd"), os.path.join(home_config_dir, "sxhkd"))
    copy_configs(os.path.join("..", "src", "polybar"), os.path.join(home_config_dir, "polybar"))

    # Копирование скрипта смены обоев в ~/bin
    bin_dir = os.path.expanduser("~/bin")
    if not os.path.exists(bin_dir):
        os.makedirs(bin_dir)  # Создаем директорию, если её нет
    shutil.copy(os.path.join("..", "src", "script", "random_wallpaper.sh"), os.path.join(bin_dir, "random_wallpaper.sh"))
    os.chmod(os.path.join(bin_dir, "random_wallpaper.sh"), 0o755)

    # Копирование папки с обоями в ~/.config
    wallpapers_src = os.path.join("..", "src", "wallpapers")
    wallpapers_dest = os.path.join(home_config_dir, "wallpapers")
    if os.path.exists(wallpapers_dest):
        shutil.rmtree(wallpapers_dest)  # Удаляем старую папку, если она существует
    shutil.copytree(wallpapers_src, wallpapers_dest)

    # Копирование .xinitrc в домашнюю директорию
    xinitrc_src = os.path.join("..",".xinitrc")
    xinitrc_dest = os.path.expanduser("~/.xinitrc")
    shutil.copy(xinitrc_src, xinitrc_dest)


    print("Установка и настройка завершены. Вы можете запустить X-сервер с помощью 'startx'.")


# ///// DELETE CONFIG

def warning():
        choise2 = input("Удалить конфигурацию darkness? [y/n]:")
        if choise2 == "y":
            delete_configurate()
        elif choise2 == "n":
            exit(1)
        else:
            print("Неверный выбор")
        


# ------------- DELETE --------------
def delete_configurate():
    choice = input("[WARNING!!!] Вы точно желаете удалить конфигурацию darkness? [y/n] ").strip().lower()
    if choice == "y":
        delete_bspwm_setup()
    elif choice == "n":
        configs = ["~/.config/bspwm", "~/.config/sxhkd", "~/.config/polybar", "~/.config/wallpapers"]
        for config in configs:
            run_command(f"rm -rf {os.path.expanduser(config)}")
    else:
        print("Неверная команда")

def delete_bspwm_setup():
    # Удаление установленных пакетов для bspwm и сопутствующих программ
    run_command("sudo pacman -Rns --noconfirm bspwm sxhkd dmenu feh picom polybar")
    print("Удалены пакеты: bspwm, sxhkd, dmenu, feh, picom, polybar.")
    
    # Удаление конфигурационных директорий из ~/.config/
    configs = ["~/.config/bspwm", "~/.config/sxhkd", "~/.config/polybar", "~/.config/wallpapers"]
    for config in configs:
        config_path = os.path.expanduser(config)
        if os.path.exists(config_path):
            run_command(f"rm -rf {config_path}")
            print(f"Удалена директория: {config}")
        else:
            print(f"Директория {config} не найдена.")

    # Удаление .xinitrc из домашней директории
    xinitrc_path = os.path.expanduser("~/.xinitrc")
    if os.path.exists(xinitrc_path):
        run_command(f"rm -f {xinitrc_path}")
        print("Удален файл: ~/.xinitrc")
    else:
        print("Файл ~/.xinitrc не найден.")

    
    # Удаление скрипта из ~/bin/
    script_path = os.path.expanduser("~/bin/random_wallpaper.sh")
    if os.path.exists(script_path):
        run_command(f"rm -f {script_path}")
        print("Удален скрипт: ~/bin/random_wallpaper.sh")
    else:
        print("Скрипт ~/bin/random_wallpaper.sh не найден.")
    
    print("Полная очистка конфигураций и пакетов завершена.")

# ---------- DELETE --------------



if __name__ == "__main__":
    run_command("clear")

    print_ascii()
    print_help()
    choice = input("").strip()
    if choice == "1":
        main()
    elif choice == "2":
        delete_configurate()
    elif choice == "3":
        exit(0)
    else:
        print("Неверный выбор")
        exit(1)
