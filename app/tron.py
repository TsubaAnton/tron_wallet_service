from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import HTTPProvider
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

TRON_API_KEY = os.getenv("TRON_API_KEY")

client = Tron(provider=HTTPProvider(api_key=TRON_API_KEY))


def get_wallet_info(address: str) -> dict:
    try:
        resources = client.get_account_resource(address)
        account = client.get_account(address)
        bandwidth = resources.get("free_net_limit", 0)
        energy = resources.get("EnergyLimit", 0)
        trx_balance = account.get("balance", 0) / 1_000_000
        return {
            "id": 0,
            "address": address,
            "bandwidth": bandwidth,
            "energy": energy,
            "trx_balance":  round(trx_balance, 6)
        }
    except AddressNotFound:
        raise ValueError("Invalid address")
