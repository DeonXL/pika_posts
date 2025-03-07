from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.keyboards import get_posts_kb

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
                        text="<b>Здарова фраер!</b>\n"
                        "Отправь <b><i>/post</i></b> и я пришлю одну из своих цитат.\n", 
                        parse_mode='HTML', 
                        reply_markup=get_posts_kb())
    