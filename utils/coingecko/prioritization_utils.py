import math
from typing import Dict, Any
from config import settings

def calculate_priority_enhanced(
    coin_data: Dict[str, Any],
    exchanges_flags: Dict[str, bool],
    alt_exchanges: list[str],
    networks: list[str],
) -> float:

    md = coin_data.get("market_data") or {}

    vol = (md.get("total_volume") or {}).get("usd") or 0
    norm_vol = math.log1p(vol)

    mc = (md.get("market_cap") or {}).get("usd") or 0
    norm_mc = math.log1p(mc)

    change24 = md.get("price_change_percentage_24h") or 0
    change7 = md.get("price_change_percentage_7d") or 0
    price_change_score = (change24 * 0.6 + change7 * 0.4)

    ath_usd = (md.get("ath") or {}).get("usd")
    current_usd = (md.get("current_price") or {}).get("usd")
    ath_drop = 0.0
    if ath_usd and current_usd and ath_usd > 0:
        ath_drop = 1.0 - (current_usd / ath_usd)

    networks_count = len(networks or [])
    networks_score = min(networks_count, settings.MAX_NETWORKS_COUNT) / settings.MAX_NETWORKS_COUNT

    key_ex_count = sum(1 for v in (exchanges_flags or {}).values() if v)
    max_key_ex = len(exchanges_flags or {}) or 1
    exchange_score = key_ex_count / max_key_ex

    alt_count = len(alt_exchanges or [])
    alt_score = min(alt_count, settings.MAX_ALTERNATIVE_EXCHANGES_COUNT) / settings.MAX_ALTERNATIVE_EXCHANGES_COUNT

    score = (
        settings.WEIGHTS["volume"] * norm_vol +
        settings.WEIGHTS["market_cap"] * norm_mc +
        settings.WEIGHTS["price_change"] * (price_change_score / 100) +
        settings.WEIGHTS["ath_drop"] * (1.0 - ath_drop) +
        settings.WEIGHTS["networks"] * networks_score +
        settings.WEIGHTS["exchanges_key"] * exchange_score +
        settings.WEIGHTS["alt_exchanges"] * alt_score
    )

    return round(score, 4)
