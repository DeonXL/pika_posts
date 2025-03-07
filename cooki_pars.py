import pickle
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import base64
import os
from db.database import session, Posts

url = 'https://pikabu.ru/'


def download_images():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()

        # Загрузка куки из файла
        with open('pikabu_cookies.pkl', 'rb') as f:
            cookies = pickle.load(f)
        context.add_cookies(cookies)

        page = context.new_page()

        
        page.goto(url)
        html= page.content()
        soup = BeautifulSoup(html, 'html.parser')
        pages = soup.find('div', class_='pagination__pages').findAll('a')
        pages = 5 #[page.get_text() for page in pages][-2]
        print(pages)

        img_urls= []
        for page_num in range(1, int(pages)+1):
            page.goto(url + f'&page={page_num}')
            i=0
            print(f'{page_num}')
            # Прокрутка браузера вниз
            for i in range(1000):
                page.mouse.wheel(0, 100)
                time.sleep(.1)

            # Ожидание загрузки содержимого страницы
            time.sleep(15)

            # Дождаться загрузки страницы
            page.wait_for_load_state('commit')

            html = page.content()
            soup = BeautifulSoup(html, 'html.parser')
            posts = soup.find_all('article') #, class_='stories-feed__container')

            # Скачивание изображений
            for i, post in enumerate(posts):
                images = post.find_all('img', class_='story-image__image')
                print(len(images))
                imgs = []
                for j, img in enumerate(images):
                    # print(f'это переменная j = {j}')
                    if img.get('src') is not None:
                        img_id = post.get('data-story-id')
                        img_url = img.get('src').split(',')[1]

                        # print(f'переменная i = {i} \n переменная j= {j}')
                        imgs.append([img_id, img_url])
                img_urls.append(imgs)



        # формируем список если картинка не одна тогда записываем через запятую под одним img_id
        # Создаем словарь для хранения айди и значений
        id_values = {}

        # Проходимся по списку и заполняем словарь
        for i in img_urls:
            for j in i:
                id_value = j[0]
                value = j[1]
                if id_value in id_values:
                    id_values[id_value].append(value)
                else:
                    id_values[id_value] = [value]
        # Обрезаем список до 10 элементов
        for key in id_values:
            id_values[key] = id_values[key][:10]
            
        # Перформатируем словарь в список
        formatted_list = []
        for id_value, values in id_values.items():
            formatted_list.append([id_value, ','.join(values)])

        # with open('tt.py', 'w', encoding='utf-8') as f:
        #     f.write(formatted_list)

        browser.close()
        # записываем в бд
        write_to_db(formatted_list)

def write_to_db(img_urls):
    for img_id, img_url in img_urls:
        print(img_id)
        existing_img = session.query(Posts).filter_by(img_id=img_id).first()
        if existing_img is None:
            new_img = Posts(img_id=img_id, img=img_url)
            session.add(new_img)
    session.commit()

download_images()