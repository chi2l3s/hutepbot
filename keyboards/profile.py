from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from hutep_vpn.schemas import VpnClient
from config import VPN_BASE_SUB

def profile_kb(client: VpnClient) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    if client:
        sub_url = f'{VPN_BASE_SUB}/{client.sub_id}'

        kb.button(text='🛜 Подключить', url=sub_url)
        kb.button(text='⌛ Продлить подписку', callback_data='purchase')
    else:
        kb.button(text='🛒 Купить подписку', callback_data='purchase')

    kb.button(text="◀️ Назад", callback_data="back_main")

    kb.adjust(1)

    return kb.as_markup()

