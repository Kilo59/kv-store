"""
This module is filled with a lot of YAGI features.
Originally was wanting to setup this API to pull from any level of the hierarchical
structures it stores rather than just the root keys/namespaces.
OpenAPI doesn't support these types of recursive paths so I dropped it for now.
But I kept in some of the features in case I want to use query params to drill down into
the data.
"""

import abc
import functools
import string
from pprint import pformat as pf
from typing import Optional

import glom_dict as gd


class Repository(abc.ABC):
    """Abstract Repository class"""

    @abc.abstractmethod
    def add(self, content, namespace: Optional[str] = None, backfill: bool = False):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, namespace: str):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, namespace: str):
        raise NotImplementedError

    @abc.abstractmethod
    def truncate(self):
        """Deallocate the root namespace for the given tenant and make ready for re-use."""
        raise NotImplementedError


@functools.lru_cache(maxsize=32)
def namespace_path(namespace: str, *extras: str) -> gd.Path:
    """Buildup a `glom.Path` objects from namespace strings."""
    paths = []
    if namespace:
        if isinstance(namespace, str):
            tokens = [p for p in namespace.split("/") if p]
            paths.extend(tokens)
        if extras:
            paths.append(namespace_path(*extras))
    return gd.Path(*paths)


SEED_DATA = {
    "seed": {
        "foo": "bar",
        "abc": list(string.ascii_lowercase),
        "deeply": {"nested": ["values", {"hello": "world"}]},
    }
}


class InMemoryRepository(Repository):
    # all instances share the same underlying data storage object
    # WARNING: not thread or multi-process safe
    _data = gd.GlomDict()

    def __init__(self, tenant: str = "root"):
        self.tenant = tenant
        if self.tenant in self._data:
            return
        self.add(SEED_DATA)

    def add(self, content, namespace: Optional[str] = None, backfill: bool = False):
        missing = dict if backfill else None
        combined_path = namespace_path(self.tenant, namespace)
        self._data.assign(combined_path, content, missing=missing)

    def get(self, namespace: str):
        return self._data[namespace_path(self.tenant, namespace)]

    def delete(self, namespace: str):
        combined_path = namespace_path(self.tenant, namespace)
        item = self.get(namespace)
        self._data.assign(combined_path, None)
        return item

    def truncate(self):
        self._data[self.tenant] = None

    def __str__(self):
        sep = "=" * len(self.__class__.__name__ + self.tenant)
        tenant_data = self._data[self.tenant]
        data_preview = f"\n{sep}\n{pf({self.tenant: tenant_data}, depth=2)}\n{sep}"
        return f"{self.__class__.__name__}('{self.tenant}'):{data_preview}"
