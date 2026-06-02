from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.terms import terms_keyboard

router = Router(name='terms')

@router.message(Command('terms'))
async def command_terms(message: Message):
    await message.answer('Ознакомьтесь с нашей политикой перед использованием:', reply_markup=terms_keyboard())