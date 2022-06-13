"""
Global test fixtures
"""
import glom_dict as gd
import pytest
from starlite import TestClient

from kv_store.api.main import app
from kv_store.api.repository import InMemoryRepository, Repository

# pylint: disable=fixme


_REPOSITORIES: list[Repository] = [
    InMemoryRepository(),
    InMemoryRepository("test_tenant"),
]


@pytest.fixture(scope="function", params=_REPOSITORIES)
def repo_param_fxt(request):
    """
    Parametrized fixture of all supported repositories.
    Creates a test case for repository.
    Cleanup after each test.
    """
    repo: Repository = request.param
    yield repo
    repo.truncate()


@pytest.fixture(scope="function")
def test_client():
    with TestClient(app=app) as client:
        yield client
