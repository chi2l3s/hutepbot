from aiohttp import web
from loguru import logger
from clients.platega.schemas import CallbackPayload

async def platega_webhook(request: web.Request) -> web.Response:
    try:
        data = await request.json()    
        webhook = CallbackPayload.from_dict(data)
        logger.debug(f'Platega Webhook: {webhook}')
        
        if webhook.is_confirmed and webhook.payload:
            plan_key, user_id = webhook.payload.split(':')
            
            bot = request.app['bot']
            session_factory = request.app['session_factory']
            
            async with session_factory() as session:
                from services.subscription import activate_subscription
                from constants import PLANS
                
                plan = PLANS[plan_key]
                
                await activate_subscription(
                    session=session,
                    user_id=int(user_id),
                    plan_key=plan_key,
                    amount=plan_key['price'],
                    provider='card'
                )
                
            await bot.send_message(
                chat_id=int(user_id),
                text='✅ Оплата подтверждена! Подписка активирована.'
            )
            
        return web.json_response(status=200)
    except Exception as e:
        logger.error(f'Ошибка обработки webhook: {e}')