#!/bin/bash

# Путь к директории с обоями
WALLPAPER_DIR="$HOME/.config/wallpapers"

# Случайный выбор обоев
WALLPAPER=$(find "$WALLPAPER_DIR" -type f | shuf -n 1)

# Установка обоев с помощью feh
feh --bg-scale "$WALLPAPER"
