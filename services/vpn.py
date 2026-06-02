import json
from loguru import logger
from hutep_vpn.client import AuthenticatedClient
from hutep_vpn.api.clients import (
    get_panel_api_clients_get_email,
    get_panel_api_clients_list,
    post_panel_api_clients_add,
    post_panel_api_clients_update_email,
)
from hutep_vpn.models.post_panel_api_clients_add_body import PostPanelApiClientsAddBody
from hutep_vpn.models.post_panel_api_clients_update_email_body import PostPanelApiClientsUpdateEmailBody
from hutep_vpn.schemas import VpnClient
from config import VPN_BASE_URL, VPN_API_TOKEN

class VpnService:
    def __init__(self):
        self.client = AuthenticatedClient(
            base_url=VPN_BASE_URL,
            token=VPN_API_TOKEN,
            verify_ssl=False
        )

    async def get_all_clients(self) -> list[VpnClient] | None:
        try:
            response = await get_panel_api_clients_list.asyncio_detailed(
                client=self.client
            )
            data = json.loads(response.content)

            if not data.get('success'):
                return None
            
            obj = data.get('obj', {})

            clients = [VpnClient.from_dict(item) for item in obj]

            return clients
        except Exception as e:
            logger.error(f'Ошибка получения списка клиентов: {e}')
            return None

    async def get_client(self, email: str) -> VpnClient | None:
        try:
            response = await get_panel_api_clients_get_email.asyncio_detailed(
                client=self.client,
                email=email
            )
            data = json.loads(response.content)

            if not data.get('success'):
                return None
            
            client = data.get('obj', {})
            return VpnClient.from_dict(client)
        except Exception as e:
            logger.error(f'Ошибка получения клиента {email}: {e}')
            return None
        
    async def create_client(self, telegram_id: int, expiry_ms: int) -> dict | None:
        try:
            response = await post_panel_api_clients_add.asyncio_detailed(
                client=self.client,
                body=PostPanelApiClientsAddBody.from_dict({
                    "client": {
                        "email": str(telegram_id),
                        "expiryTime": expiry_ms,
                        "enable": True,
                        "tgId": telegram_id
                    },
                    "inboundIds": [
                        4
                    ]
                })
            )
            return json.loads(response.content)
        except Exception as e:
            logger.error(f'Ошибка создания VPN клиента {telegram_id}: {e}')
            return None

    async def update_expiry(self, telegram_id: int, expiry_ms: int) -> bool:
        try:
            response = await post_panel_api_clients_update_email.asyncio_detailed(
                client=self.client,
                email=str(telegram_id),
                body=PostPanelApiClientsUpdateEmailBody.from_dict({
                    "email": str(telegram_id),
                    "expiryTime": expiry_ms,
                    "enable": True,
                    "tgId": telegram_id,
                })
            )
            data = json.loads(response.content)
            return bool(data.get('success'))
        except Exception as e:
            logger.error(f'Ошибка продления VPN клиента {telegram_id}: {e}')
            return False

vpn_service = VpnService()