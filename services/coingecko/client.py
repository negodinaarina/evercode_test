from services.base import BaseClient

TARGET_EXCHANGES = {"binance", "bybit", "kucoin"}

class CoinGeckoClient(BaseClient):
    async def get_coin_detailed_data(self, coin_id: str):
        """
        Получить подробную информацию по монете
        """
        return await self._get(url=f"/coins/{coin_id}")

    async def get_top_by_volume(self, limit: int = 100):
        """
        Получение топ-активов по объему торгов за 24 часа через CoinGecko
        """
        url = "/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "volume_desc",
            "per_page": limit,
            "page": 1,
        }
        return await self._get(url, params=params)

    async def get_top_by_listing_date(self, limit: int = 100):
        """
        Получение топ-активов по дате листинга через CoinGecko
        (CoinGecko напрямую не сортирует по дате, используем id как приближение)
        """
        url = "/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "id",
            "per_page": limit,
            "page": 1,
        }
        return await self._get(url, params=params)

    async def get_exchanges(self, coin_id: str):
        """
        Получение списка бирж, где торгуется монета, через CoinGecko
        """
        return (await self._get(url=f"/coins/{coin_id}/tickers")).get("tickers")


coin_gecko_client = CoinGeckoClient(
    base_url="https://api.coingecko.com/api/v3"
)
