from loguru import logger
from datetime import datetime, timezone
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError
from services.vpn import vpn_service

async def check_expiring_subscriptions(bot: Bot):
    logger.info('[CRON] Проверка подписок')
    clients = await vpn_service.get_all_clients()
    if not clients:
        return
                
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    three_days_ms = 3 * 24 * 60 * 60 * 1000

    for client in clients:
        expiry = client.expiry_time
        if expiry == 0:
            continue
        if 0 < expiry - now_ms < three_days_ms:
            try:
                tg_id = client.email
                await bot.send_message(
                    chat_id=tg_id,
                    text='⚠️ Твоя подписка истекает менее чем через 3 дня\n\n'
                    'Продли, чтобы не потерять доступ'
                )
            except TelegramAPIError:
                logger.warning(f'Пользователь {tg_id} заблокировал бота или не существует')