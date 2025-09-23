from abc import ABC, abstractmethod
from typing import Any, Dict

class ParserInterface(ABC):
    @staticmethod
    @abstractmethod
    async def parse_coin_exchanges(coin_id: str) -> Dict[str, Any]:
        pass

    @staticmethod
    @abstractmethod
    async def parse_coin_networks(coin_data: Dict[str, Any]) -> Any:
        pass