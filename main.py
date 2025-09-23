import asyncio
from utils.report_builder import ReportBuilder
from services.coingecko.client import coin_gecko_client
from utils.coingecko.parser import coin_gecko_parser
from utils.coingecko.prioritization_utils import calculate_priority_enhanced
from utils.file_utils import export_full_report

if __name__ == "__main__":
    report_builder = ReportBuilder(
        prioritizer=calculate_priority_enhanced,
        parser=coin_gecko_parser,
        source_client=coin_gecko_client
    )
    full_report = asyncio.run(report_builder.build_full_report())
    asyncio.run(export_full_report(full_report))
