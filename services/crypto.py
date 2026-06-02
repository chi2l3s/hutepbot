from aiocryptopay import AioCryptoPay, Networks
from config import CRYPTO_BOT_TOKEN
from loguru import logger
import aiohttp

crypto: AioCryptoPay = None

def get_crypto_client() -> AioCryptoPay:
    global crypto
    if crypto is None:
        crypto = AioCryptoPay(
            token=CRYPTO_BOT_TOKEN,
            network=Networks.TEST_NET
        )
    return crypto

async def get_usd_rate() -> float:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.exchangerate-api.com/v4/latest/USD') as r:
            data = await r.json()
            return data['rates']['RUB']

async def create_invoice(amount: float, plan_key: str, user_id: int) -> str:
    usd_rate = await get_usd_rate()
    amount_usd = round(amount / usd_rate, 2)

    invoice = await crypto.create_invoice(
        currency_type='fiat',
        fiat='USD',
        amount=amount_usd,
        description='VPN подписка',
        payload=f'{plan_key}:{user_id}'
    )
    return invoice.mini_app_invoice_url

async def check_payment(plan_key: str, user_id: int) -> str | None:
    invoices = await crypto.get_invoices(status='paid')

    if not invoices:
        return None

    target = f'{plan_key}:{user_id}'
    for inv in invoices:
        if inv.payload == target:
            return str(inv.invoice_id)
    return None