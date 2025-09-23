from typing import Any

from config import settings

def parse_exchanges(exchanges_list: list[str]):
    """
    Функция для анализа бирж.

    :param exchanges_list: список всех бирж, где торгуется актив (строки)
    :param target_exchanges: список ключевых бирж для проверки
    :return:
        1. Словарь флагов ключевых бирж {биржа: True/False}
        2. Список альтернативных бирж (неключевых), уникальные
    """

    all_exchanges = [ex.lower() for ex in exchanges_list]

    exchanges_flags = {ex.lower(): ex.lower() in all_exchanges for ex in settings.TARGET_EXCHANGES}

    alt_exchanges = sorted({ex for ex in all_exchanges if ex.lower() not in map(str.lower, settings.TARGET_EXCHANGES)})

    return {"base_exchanges": exchanges_flags, "alternative_exchanges": alt_exchanges}

def parse_networks(platforms: dict[str, Any], coin_id: str):
    """
    Определяет, в каких блокчейн-сетях доступен токен.
    Для токенов возвращает список сетей (Ethereum, BNB Chain, Solana и т.д.).
    Для Layer-1 монет (BTC, ETH, SOL) возвращает их собственную сеть.
    """
    valid_networks = [net.lower() for net, addr in platforms.items() if addr and net.strip() and str(addr).strip()]
    if valid_networks:
        return sorted(list(dict.fromkeys(valid_networks)))
    return [coin_id, ]