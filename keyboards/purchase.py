from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from constants import PLANS

def plans_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for key, plan in PLANS.items():
        kb.button(text=f"{plan['label']} — {plan['price']} ₽", callback_data=key)
    kb.button(text="◀️ Назад", callback_data="back_main")
    kb.adjust(1)
    return kb.as_markup()

def payment_methods_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(text="⭐️ Telegram Stars", callback_data="pay_stars")
    kb.button(text="💳 Карта", callback_data="pay_card")
    kb.button(text="₿ Крипта", callback_data="pay_crypto")
    kb.button(text="◀️ Назад", callback_data="back_plans")

    kb.adjust(1)
    return kb.as_markup()