import aiohttp
from loguru import logger
from config import PLATEGA_BASE_URL, PLATEGA_MERCHANT_ID, PLATEGA_SECRET_KEY

class PlategaClient:
    def __init__(self):
        self.base_url = PLATEGA_BASE_URL
        self.headers = {
            'X-MerchantId': PLATEGA_MERCHANT_ID,
            'X-Secret': PLATEGA_SECRET_KEY
        }
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=self.base_url,
                headers=self.headers
            )
        return self._session
    
    async def _get(self, path: str, params: dict | None = None) -> dict:
        session = await self._get_session()
        async with session.get(path, params=params) as response:
            response.raise_for_status()
            return await response.json()
        
    async def _post(self, path: str, body: dict | None = None):
        session = await self._get_session()
        async with session.post(path, json=body) as response:
            response.raise_for_status()
            return await response.json()
        
    async def close(self):
        if self._session:
            await self._session.close()