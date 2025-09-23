from typing import Any

from utils.base.parse_utils import parse_exchanges, parse_networks
from services.coingecko.client import coin_gecko_client
from utils.base.parser import ParserInterface

class CoinGeckoParser(ParserInterface):

    @staticmethod
    async def parse_coin_exchanges(coin_id: str):
        """
        Получает данные монеты от CoinGecko и возвращает:
        {
            "exchanges_flags": dict,
            "alt_exchanges": list,
        }
        """
        tickers_resp = await coin_gecko_client.get_exchanges(coin_id)
        if not isinstance(tickers_resp, list):
            tickers_resp = []
        all_exchanges = [
            t.get("market", {}).get("name")
            for t in tickers_resp
            if t.get("market", {}).get("name")
        ]
        return parse_exchanges(all_exchanges)

    @staticmethod
    async def parse_coin_networks(coin_data: dict[str, Any]):
        """
        Получает данные монеты от CoinGecko и возвращает:
        {
            "networks": list
        }
        """
        platforms = coin_data.get("platforms", {})
        return parse_networks(platforms, coin_data.get("id"))

coin_gecko_parser = CoinGeckoParser()