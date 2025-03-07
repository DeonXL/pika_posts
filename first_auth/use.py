# use.py
import requests
import pickle
from bs4 import BeautifulSoup

# Функция для загрузки куки и проверки авторизации
def load_session_and_parse():
    try:
        # Загружаем куки из файла
        with open('pikabu_cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)

        # Создаем новую сессию и загружаем куки
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        # Переходим на страницу настроек для проверки авторизации
        response = session.get('https://pikabu.ru/settings')
        soup = BeautifulSoup(response.text, 'html.parser')

        # Проверяем наличие блока с предупреждением о необходимости авторизации
        auth_warning = soup.find('div', class_='app__warning')
        if auth_warning:
            print('Ошибка авторизации: Пожалуйста, авторизуйтесь или зарегистрируйтесь.')
            return False  # Куки недействительны
        else:
            print('Авторизация успешна!')
            return True  # Куки действительны
    except Exception as e:
        print(f"Ошибка: {e}")
        return False  # Файл с куками не найден или произошла ошибка