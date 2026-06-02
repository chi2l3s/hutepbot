from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def terms_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Политика конфиденциальности', url='https://telegra.ph/Politika-konfidencialnosti-04-01-26')
    builder.button(text='Пользовательское соглашение', url='https://telegra.ph/Polzovatelskoe-soglashenie-04-01-19')

    builder.adjust(1)

    return builder.as_markup()