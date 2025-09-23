from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корневая директория проекта
ROOT_DIR = Path(__file__).resolve(strict=True).parent

# Папка для вывода отчетов
OUTPUT_DIR = ROOT_DIR / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseSettings):
    """
    Настройки проекта и параметров работы с API.
    """
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR.parent / ".env",  # Файл окружения для подгрузки переменных
        case_sensitive=True,
        extra="allow"  # Разрешить дополнительные переменные окружения
    )

    # CoinGecko API настройки
    COIN_GECKO_KEY: str = ""  # API-ключ для CoinGecko (если требуется, должен браться из .env и передаваться при создании объекта класса-клиента в headers)
    COIN_GECKO_URL: str = "https://api.coingecko.com/api/v3"  # Базовый URL API
    COINGECKO_MAX_REQUESTS_PER_MINUTE: int = 25  # Лимит запросов к CoinGecko в минуту

    # Настройки параметров базового HTTP клиента и ретраев
    MAX_RETRIES: int = 1  # Количество повторных попыток запроса при ошибке
    RETRY_MULTIPLIER: int = 5  # Множитель для увеличения времени ожидания между повторными попытками
    MIN_RETRY_DELAY: int = 1  # Минимальная задержка перед повторным запросом (секунды)
    MAX_RETRY_DELAY: int = 60  # Максимальная задержка перед повторным запросом (секунды)
    MAX_CONNECTIONS: int = 100  # Максимальное количество одновременных соединений
    MAX_KEEPALIVE: int = 40  # Время поддержания keep-alive соединений (секунды)
    READ_TIMEOUT: int = 100  # Таймаут на чтение ответа (секунды)
    CONNECT_TIMEOUT: int = 20  # Таймаут на подключение (секунды)
    WRITE_TIMEOUT: int = 100  # Таймаут на отправку запроса (секунды)
    POOL_TIMEOUT: int = 50  # Таймаут ожидания свободного соединения из пула (секунды)
    REQUEST_PER_MINUTE: int = 30  # Общий лимит запросов в минуту для клиента

    # Настройки бирж и лимитов отчета
    TARGET_EXCHANGES: set = {"binance", "bybit", "kucoin"}  # Основные целевые биржи для анализа
    REPORT_LIMIT: int = 100  # Количество топовых монет для формирования отчета

    # Веса для расчета приоритета монет
    WEIGHTS: dict = {
        "volume": 0.2,             # Влияние объема торгов
        "market_cap": 0.2,         # Влияние рыночной капитализации
        "price_change": 0.1,       # Влияние изменения цены (24ч/7д)
        "ath_drop": 0.1,           # Влияние падения от ATH
        "networks": 0.1,           # Влияние количества сетей
        "exchanges_key": 0.1,      # Влияние наличия монеты на ключевых биржах
        "alt_exchanges": 0.05      # Влияние альтернативных бирж
    }

    # Ограничения для расчета приоритета
    MAX_NETWORKS_COUNT: int = 2  # Максимальное количество сетей для учета
    MAX_ALTERNATIVE_EXCHANGES_COUNT: int = 10  # Максимальное количество альтернативных бирж для учета

# Экземпляр настроек для использования в проекте
settings = Settings()
