from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from config import BOT_TOKEN, WEBHOOK_URL
from handlers import start, terms, support, profile, purchase
from handlers.webhooks.platega import platega_webhook
from middlewares.db import DbSessionMiddleware
from db.base import SessionLocal
from logger import setup_logger
from scheduler import setup_scheduler

logger = setup_logger()

async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL)
    logger.info(f'Webhook установлен на: {WEBHOOK_URL}')
    
    setup_scheduler(bot)
    
    from services.crypto import get_crypto_client
    get_crypto_client()

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logger.info('Webhook успешно удален.')

def main():
    logger.info('Запуск бота...')

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(SessionLocal))

    dp.include_router(start.router)
    dp.include_router(terms.router)
    dp.include_router(support.router)
    dp.include_router(profile.router)
    dp.include_router(purchase.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    
    app['bot'] = bot
    app['session_factory'] = SessionLocal

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_request_handler.register(app, path='/webhook')
    
    app.router.add_post('/webhooks/platega', platega_webhook)

    setup_application(app, dp, bot=bot) 

    logger.info('Запуск веб сервера...')
    logger.success('Бот успешно подготовлен к запуску!')
    
    web.run_app(app, host='0.0.0.0', port=8000)

if __name__ == "__main__":
    main()