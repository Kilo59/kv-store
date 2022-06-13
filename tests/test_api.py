import pytest
from starlite import TestClient


@pytest.mark.parametrize("path", ["/", "/schema", "/health", "/names", "/names/seed"])
def test_health(test_client: TestClient, path: str):
    response = test_client.get(path)
    print(response)
    assert response.status_code == 200


@pytest.mark.parametrize(
    "method,path,req_kws,expected_status",
    [
        ("PUT", "/names/test_1", {"json": {"hello": "world"}}, 200),
        ("PUT", "/names/test_2", {"json": "hello world"}, 200),
        ("PUT", "/names/test_3", {"json": ["hello", "world"]}, 200),
        ("PUT", "/names/test_4", {"json": {"a": {"b": {"c": "hello world"}}}}, 200),
        ("DELETE", "/names/seed", {}, 200),
    ],
)
class TestMethods:
    def test_status_codes(
        self,
        test_client: TestClient,
        method: str,
        path: str,
        req_kws: dict,
        expected_status,
    ):
        initial_r = test_client.request(method, path, **req_kws)
        print(initial_r)
        initial_r.raise_for_status()

        final_r = test_client.get(path)
        print(final_r)
        assert expected_status == final_r.status_code

    def test_details(
        self,
        test_client: TestClient,
        method: str,
        path: str,
        req_kws: dict,
        expected_status,
    ):
        initial_r = test_client.request(method, path, **req_kws)
        print(initial_r)
        initial_r.raise_for_status()

        final_r = test_client.get(path)
        print(f"{final_r}\n{final_r.json()}")
        assert req_kws.get("json") == final_r.json()


if __name__ == "__main__":
    pytest.main(["-vv"])
