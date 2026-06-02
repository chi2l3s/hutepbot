from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

DATABASE_URL = os.getenv('DATABASE_URL')

VPN_BASE_URL = os.getenv('VPN_BASE_URL')
VPN_API_TOKEN = os.getenv('VPN_API_TOKEN')
VPN_BASE_SUB = os.getenv('VPN_BASE_SUB')

CRYPTO_BOT_TOKEN = os.getenv('CRYPTO_BOT_TOKEN')