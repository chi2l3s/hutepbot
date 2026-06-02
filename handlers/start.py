from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.repository import get_or_create_user
from keyboards.main import main_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message, session: AsyncSession):
    user = await get_or_create_user(
        session,
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name
    )
    await message.answer(
        f'<b>{user.full_name}</b>, привет 👋\n\n'
        '🔒 Твой личный VPN — всегда на связи.\n'
        'Настрой, подключись, забудь что бывают проблемы.\n\n'
        'Возник вопрос? - Обратись в поддержку\n\n'
        '👇',
        reply_markup=main_keyboard(),
    )