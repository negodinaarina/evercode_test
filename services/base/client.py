import enum
from typing import Any, Union

from httpx import AsyncClient, ConnectTimeout, Limits, ReadTimeout, Timeout
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from config import settings
from services.base.exceptions import ClientException


class HTTPMethods(enum.StrEnum):
    GET = enum.auto()
    POST = enum.auto()


ResponseType = Union[list, dict]


class BaseClient:
    def __init__(
        self, base_url: str, headers: dict[str, Any] | None = None
    ) -> None:
        self._base_url = base_url
        self._headers = headers or {}
        self._client = AsyncClient(
            base_url=self._base_url,
            headers=self._headers,
            timeout=Timeout(
                connect=settings.CONNECT_TIMEOUT,
                read=settings.READ_TIMEOUT,
                write=settings.WRITE_TIMEOUT,
                pool=settings.POOL_TIMEOUT,
            ),
            limits=Limits(
                max_connections=settings.MAX_CONNECTIONS,
                max_keepalive_connections=settings.MAX_KEEPALIVE,
            ),
        )

    @staticmethod
    def is_retryable_exception(exc: Exception) -> bool:
        return (
            (isinstance(exc, ClientException) and exc.status_code == 429)
            or isinstance(exc, ReadTimeout)
            or isinstance(exc, ConnectTimeout)
        )

    @retry(
        retry=retry_if_exception(is_retryable_exception),
        wait=wait_exponential(
            multiplier=settings.RETRY_MULTIPLIER,
            min=settings.MIN_RETRY_DELAY,
            max=settings.MAX_RETRY_DELAY,
        ),
        stop=stop_after_attempt(settings.MAX_RETRIES),
        reraise=True,
    )
    async def _make_request(
        self,
        method: HTTPMethods,
        url: str,
        **kwargs,
    ) -> ResponseType:
        response = await self._client.request(
            method=method,
            url=url,
            **kwargs,
        )

        if response.status_code >= 300:
            raise ClientException(
                status_code=response.status_code,
                detail=response.text,
            )

        return response.json()

    async def _get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        **kwargs,
    ) -> ResponseType:
        return await self._make_request(
            method=HTTPMethods.GET,
            url=url,
            params=params,
            **kwargs,
        )