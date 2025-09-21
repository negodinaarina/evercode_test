from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).resolve(strict=True).parent

LOGS_DIR = ROOT_DIR.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

BENCHMARKS_DIR = ROOT_DIR.parent / "output"
BENCHMARKS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR.parent / ".env", case_sensitive=True, extra="allow"
    )
    #CoinMarketCapClient настройки
    COIN_MARKET_CAP_KEY: str = 'f7ab4378-d248-4c4a-aa37-367efe216354'
    COIN_MARKET_CAP_URL: str = "https://pro-api.coinmarketcap.com/v1"

    # Настройки параметров базового клиента и ретраев
    MAX_RETRIES: int = 3
    RETRY_MULTIPLIER: int = 1
    MIN_RETRY_DELAY: int = 1
    MAX_RETRY_DELAY: int = 60
    MAX_CONNECTIONS: int = 100
    MAX_KEEPALIVE: int = 40
    READ_TIMEOUT: int = 100
    CONNECT_TIMEOUT: int = 20
    WRITE_TIMEOUT: int = 100
    POOL_TIMEOUT: int = 50

    TARGET_EXCHANGES: set = {"binance", "bybit", "kucoin"}



settings = Settings()
