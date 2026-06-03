from ..client import PlategaClient
from ..schemas import CreateTransactionBody, CreateTransactionResponse

async def create_transaction(client: PlategaClient, body: CreateTransactionBody) -> CreateTransactionResponse:
    data = await client._post('/v2/transaction/process', body=body.to_dict())
    return CreateTransactionResponse.from_dict(data)