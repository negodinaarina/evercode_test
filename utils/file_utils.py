import csv
from typing import Any
import asyncio
from datetime import datetime
from config import OUTPUT_DIR

def export_coins_to_csv(coins: list[dict[str, Any]], filename: str) -> None:
    """
    Сохраняет список монет в CSV файл.
    Для каждой монеты:
      - отдельные колонки под биржи из base_exchanges (True/False)
      - колонка alternative_exchanges (список альтернативных бирж)
      - колонка networks (список сетей)

    :param coins: список словарей-отчетов по монетам
    :param filename: имя файла для сохранения
    """

    all_base_exchanges: set[str] = set()
    for coin in coins:
        base_ex = coin.get("exchanges", {}).get("base_exchanges", {})
        all_base_exchanges.update(base_ex.keys())

    fieldnames = ["coin_id", "priority_score", "networks", "alternative_exchanges"]
    fieldnames[2:2] = sorted(all_base_exchanges)

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for coin in coins:
            row = {
                "coin_id": coin.get("coin_id"),
                "priority_score": coin.get("priority_score", ""),
                "networks": ", ".join(coin.get("networks", [])),
                "alternative_exchanges": ", ".join(
                    coin.get("exchanges", {}).get("alternative_exchanges", [])
                ),
            }

            base_exchanges = coin.get("exchanges", {}).get("base_exchanges", {})
            for ex in all_base_exchanges:
                row[ex] = base_exchanges.get(ex, False)

            writer.writerow(row)

async def export_full_report(report: dict[str, list[dict]]) -> None:
    """
    Формирует имена CSV файлов из типа списка и даты/времени генерации отчета,
    и передает списки монет в export_coins_to_csv. Файлы создаются параллельно.

    :param report: full report, словарь с ключами типа "top-100-by-volume" и "top-100-by-listing-date"
    """

    async def export_list(coins: list[dict], report_type: str):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{OUTPUT_DIR}/{report_type}_{timestamp}.csv"
        await asyncio.to_thread(export_coins_to_csv, coins, filename)

    tasks = []
    for report_type, coins in report.items():
        tasks.append(export_list(coins, report_type))

    await asyncio.gather(*tasks)
