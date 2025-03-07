import tempfile
import os
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from sqlalchemy import func
import base64
import io

from db.database import session, Posts

router = Router()

@router.message(Command(commands=['post']))
@router.message(F.text.lower() == 'пост')
async def answer_post(message: Message):
    await message.delete()
    # Получаем случайное изображение из базы данных
    img = session.query(Posts).order_by(func.random()).first().img
    print(len(img.split(',')))

    # проверяем одно изображение или несколько
    if len(img.split(',')) > 1:
        # Декодируем изображения
        images = []
        file_paths = []
        for i in img.split(','):
            binary_data = base64.b64decode(i)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(binary_data)
                temp_file_path = temp_file.name
                images.append(InputMediaPhoto(media=FSInputFile(temp_file_path), filename='image.jpg', has_spoiler=True))
                file_paths.append(temp_file_path)

        try:
            # Отправляем группу изображений
            await message.answer_media_group(media=images, has_spoiler=True)
        finally:
            # Удаляем временные файлы после отправки
            for file_path in file_paths:
                os.remove(file_path)

    else:        
        # Декодируем base64 в бинарные данные
        binary_data = base64.b64decode(img)

        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(binary_data)
            temp_file_path = temp_file.name

        try:
            # Отправляем фото из временного файла
            await message.answer_photo(photo=FSInputFile(temp_file_path, filename='1.jpg'), has_spoiler=True)
        finally:
            # Удаляем временный файл после отправки
            os.remove(temp_file_path)

    session.close()