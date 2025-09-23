import asyncio
from typing import Any, Dict, List

from config import settings


class ReportBuilder:
    """
    Класс для построения полного отчета по монетам.
    """

    def __init__(self, source_client, parser, prioritizer):
        self.client = source_client
        self.parser = parser
        self.prioritizer = prioritizer

    async def build_coin_report(self, coin_id: str) -> Dict[str, Any]:
        """
        Собирает полный отчет по одной монете:
        - подробные данные
        - биржи
        - сети
        - приоритет
        """
        coin_data = await self.client.get_coin_detailed_data(coin_id)
        exchanges = await self.parser.parse_coin_exchanges(coin_id)
        networks = await self.parser.parse_coin_networks(coin_data)

        priority_score = self.prioritizer(
            coin_data=coin_data,
            exchanges_flags=exchanges.get("base_exchanges", {}),
            alt_exchanges=exchanges.get("alternative_exchanges", []),
            networks=networks,
        )

        return {
            "coin_id": coin_id,
            "exchanges": exchanges,
            "networks": networks,
            "priority_score": priority_score,
        }

    async def build_full_report(
        self, limit: int = settings.REPORT_LIMIT
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Строит полный отчет по топ-coin по объему и дате листинга.
        """
        top_by_volume = await self.client.get_top_by_volume(limit)
        top_by_listing = await self.client.get_top_by_listing_date(limit)

        volume_ids = [coin["id"] for coin in top_by_volume]
        listing_ids = [coin["id"] for coin in top_by_listing]

        reports_by_volume, reports_by_listing = await asyncio.gather(
            asyncio.gather(*(self.build_coin_report(cid) for cid in volume_ids)),
            asyncio.gather(*(self.build_coin_report(cid) for cid in listing_ids)),
        )

        return {
            f"top-{limit}-by-volume": reports_by_volume,
            f"top-{limit}-by-listing-date": reports_by_listing,
        }
