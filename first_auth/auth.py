import sys
sys.path.append('pika_posts/')

# auth.py
import pickle
import os
from playwright.sync_api import sync_playwright
from pika_posts.config import username, password

# URL для авторизации
login_url = 'https://pikabu.ru/'

# Функция для авторизации и решения капчи
def authorize_and_save_cookies():
    with sync_playwright() as p:
        # Запускаем браузер (по умолчанию Chromium)
        browser = p.chromium.launch(headless=False)  # headless=False для видимого браузера
        context = browser.new_context()
        page = context.new_page()

        # Открываем страницу авторизации
        page.goto(login_url)

        # Вводим логин и пароль
        page.fill('input[name="username"]', username)  # Селектор для поля логина
        page.fill('input[name="password"]', password)  # Селектор для поля пароля

        # Нажимаем кнопку "Войти"
        page.click('button[type="submit"]')  # Селектор для кнопки "Войти"

        # Ждем появления капчи
        print("Решите капчу в браузере...")
        input("После решения капчи нажмите Enter...")

        # Обновляем страницу
        page.reload()

        # Получаем куки из браузера
        cookies = context.cookies()

        # Закрываем браузер
        browser.close()

        # Сохраняем куки в файл
        with open('pikabu_cookies.pkl', 'wb') as f:
            pickle.dump(cookies, f)

        print("Куки успешно сохранены!")