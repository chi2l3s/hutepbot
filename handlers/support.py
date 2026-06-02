from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.support import support_keyboard
from keyboards.main import main_keyboard

router = Router(name='support')

@router.callback_query(F.data == 'support')
async def support_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        'Если вы столкнулись с ошибкой или хотите задать вопрос — '
        'обратитесь в поддержку: @HutepVPNSupport',
        reply_markup=support_keyboard()
    )

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