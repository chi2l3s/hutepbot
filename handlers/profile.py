from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from services.vpn import vpn_service
from keyboards.profile import profile_kb
from keyboards.main import main_keyboard
from utils import format_time

router = Router(name='profile')

@router.callback_query(F.data == 'profile')
async def profile_handler(callback: CallbackQuery):
    await callback.answer()

    client = await vpn_service.get_client(callback.from_user.id)

    if client:
        expiry_ms = client.expiry_time
        await callback.message.edit_text(
            'Ваша подписка:\n\n'
            f'Статус: {'✅ Активна' if client.enable else '❌ Неактивна'}\n'
            f'Срок: активна до {format_time(expiry_ms)}',
            reply_markup=profile_kb(client)
        )
    else:
        await callback.message.edit_text('Подписка не найдена', reply_markup=profile_kb(client))

@router.callback_query(F.data == 'back_main')
async def back_main_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        f'<b>{callback.from_user.full_name}</b>, привет 👋\n\n'
        '🔒 Твой личный VPN — всегда на связи.\n'
        'Настрой, подключись, забудь что бывают проблемы.\n\n'
        'Возник вопрос? - Обратись в поддержку\n\n'
        '👇',
        reply_markup=main_keyboard()
    )