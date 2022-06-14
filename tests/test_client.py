import pytest
from starlite import TestClient

from kv_store.api.main import app
from kv_store.client import Client, HttpClient, factory


@pytest.mark.parametrize("path", ["/", "/schema", "/health", "/names", "/names/seed"])
def test_health(test_client: TestClient, path: str):
    response = test_client.get(path)
    print(response)
    assert response.status_code == 200


@pytest.mark.skip(reason="Need running api")
@pytest.mark.parametrize(
    "key,value",
    [
        ("test_1", {"hello": "world"}),
        ("test_2", "hello world"),
        ("test_3", ["hello", "world"]),
        ("test_4", {"a": {"b": {"c": "hello world"}}}),
    ],
)
class TestClientSet:
    def test_http(
        self,
        key: str,
        value: dict,
    ):
        # api must be running
        http_client = factory("http", {"base_url": "http://127.0.0.1:8000"})
        http_client.set(key, value)
        assert value == http_client.get(key)


@pytest.mark.skip(reason="Need running api")
@pytest.mark.parametrize(
    "key,value",
    [
        ("test_1", {"hello": "world"}),
        ("test_2", "hello world"),
        ("test_3", ["hello", "world"]),
        ("test_4", {"a": {"b": {"c": "hello world"}}}),
    ],
)
class TestClientDelete:
    def test_http(
        self,
        key: str,
        value: dict,
    ):
        # api must be running
        http_client = factory("http", {"base_url": "http://127.0.0.1:8000"})
        http_client.set(key, value)

        http_client.delete(key)
        post_del_result = http_client.get(key)
        print(post_del_result)
        assert not post_del_result


if __name__ == "__main__":
    pytest.main(["-vv"])
