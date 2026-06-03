from clients.platega import PlategaClient
from clients.platega.api.payments import create_transaction
from clients.platega.schemas import CreateTransactionBody, PaymentDetailsBody

client = PlategaClient()

async def create_payment_url(
    amount: float,
    plan_key: str,
    user_id: str
) -> str:
    body = CreateTransactionBody(
        payment_details=PaymentDetailsBody(amount=amount, currency='RUB'),
        payload=f'{plan_key}:{user_id}',
        description='Подписка на HutepVPN',
    )
    transaction = await create_transaction(client=client, body=body)
    return transaction.url