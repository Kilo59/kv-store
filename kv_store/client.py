"""
kv-store client
"""
import abc
import logging
import os
from typing import Any, Optional

import httpx

LOGGER = logging.getLogger(__file__)

KV_BASE_URL = os.environ.get("KV_BASE_URL", "https://py-kv-store.herokuapp.com")


class Client(abc.ABC):
    """
    Example usage

    >>> my_client["foo"] = "bar"

    >>> my_client["foo"]
    "bar"

    >>> del my_client["foo"]

    >>> my_client.pop("foo")
    "bar"

    """

    @abc.abstractmethod
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def __setitem__(self, key: str, item: Any) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def __delitem__(self, key: str):
        raise NotImplementedError

    def get(self, key) -> Any:
        return self[key]

    def set(self, key, item: Any):
        self[key] = item

    def delete(self, key):
        del self[key]


class HttpClient(Client):
    def __init__(
        self, _client: Optional[httpx.Client] = None, **async_client_kwargs
    ) -> None:
        if isinstance(_client, httpx.Client):
            self._client = _client
        else:
            config = {"base_url": KV_BASE_URL, **async_client_kwargs}
            self._client = httpx.Client(**config)

    def __getitem__(self, key: str) -> Any:
        response = self._client.get(f"/names/{key}")
        response.raise_for_status()
        return response.json()

    def __setitem__(self, key: str, item: Any) -> None:
        response = self._client.put(f"/names/{key}", json=item)
        response.raise_for_status()

    def __delitem__(self, key: str):
        response = self._client.delete(f"/names/{key}")
        response.raise_for_status()


_CLIENT_MAPPING = {"http": HttpClient}


def factory(protocol: str, config: Optional[dict] = None) -> Client:
    """Return a client instance according to provided protocol and config."""
    config = config if config else {}

    try:
        client = _CLIENT_MAPPING[protocol]
        return client(**config)
    except KeyError as exc:
        LOGGER.debug(f"{protocol=} {exc}")
        raise NotImplementedError(
            f"{protocol=} is not supported. Expected {list(_CLIENT_MAPPING.keys())}"
        )
