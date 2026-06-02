from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.button(text='Моя подписка', callback_data='profile')
    # kb_builder.button(text='Реферальная программа', callback_data='referral')
    kb_builder.button(text='Поддержка', callback_data='support')

    kb_builder.adjust(1, 2)

    return kb_builder.as_markup()