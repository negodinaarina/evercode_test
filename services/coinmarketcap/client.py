from services.base import BaseClient
from config import settings
class CoinMarketCapClient(BaseClient):

    async def get_top_by_volume(self, limit: int = 100):
        """
        Получение топ-активов по объему торгов за 24 часа
        """
        url = "/cryptocurrency/listings/latest"
        params = {
            "start": 1,
            "limit": limit,
            "sort": "volume_24h",
            "convert": "USD",
        }
        return await self._get(url, params=params)

    async def get_top_by_listing_date(self, limit: int = 100):
        """
        Получение топ-активов по дате листинга
        """
        url = "/cryptocurrency/listings/latest"
        params = {
            "start": 1,
            "limit": limit,
            "sort": "date_added",
            "convert": "USD",
        }
        return await self._get(url, params=params)

    async def get_exchanges_pairs(self, coin_id: int, limit: int = 500):
        """
        Получение биржевых пар для монеты
        """
        url = "/cryptocurrency/market-pairs/latest"
        params = {"id": coin_id, "limit": limit}
        return await self._get(url, params=params)

coin_market_cap_client = CoinMarketCapClient(
    base_url=settings.COIN_MARKET_CAP_URL,
    headers={"X-CMC_PRO_API_KEY": settings.COIN_MARKET_CAP_KEY}
)