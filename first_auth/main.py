# main.py
from auth import authorize_and_save_cookies
from use import load_session_and_parse
import os

# Проверяем, существует ли файл с куками
if os.path.exists('pikabu_cookies.pkl'):
    print("Файл с куками найден. Проверяем их валидность...")
    if load_session_and_parse():
        print("Используем сохраненные куки.")
    else:
        print("Куки недействительны. Запускаем процесс авторизации...")
        authorize_and_save_cookies()
        load_session_and_parse()
else:
    print("Файл с куками не найден. Запускаем процесс авторизации...")
    authorize_and_save_cookies()
    load_session_and_parse()