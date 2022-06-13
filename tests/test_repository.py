import copy
from pprint import pformat as pf

import glom_dict as gd
import pytest

from kv_store.api.repository import InMemoryRepository, Repository, namespace_path


@pytest.mark.parametrize(
    "namespace,extras,expected",
    [
        ("/foo/bar", [], gd.Path("foo", "bar")),
        ("/foo/bar", [None], gd.Path("foo", "bar")),
        ("foo/bar", [], gd.Path("foo", "bar")),
        ("foo", ["bar"], gd.Path("foo", "bar")),
        ("/", ["foo", "bar"], gd.Path("foo", "bar")),
        ("/a", ["b", "c", "d", None], gd.Path("a", "b", "c", "d")),
    ],
)
def test_namespace_path(namespace, extras, expected):
    assert expected == namespace_path(namespace, *extras)


def test_in_memory_repo_init():
    repo = InMemoryRepository("test_tenant")
    print(repo)
    assert "test_tenant" in repo._data


def test_in_memory_repo_trunc():
    repo = InMemoryRepository("foo")
    repo.add("bar")
    repo.truncate()
    print(repo)
    assert repo.get("/") != "bar"


@pytest.mark.parametrize(
    "content",
    [
        "foo",
        {"a": ["b", "c", "d"]},
        [{"a": 0}, {"b": 1}, {"c": 2}],
    ],
)
def test_repo_round_trip(repo_param_fxt: Repository, content):
    # copy to avoid issues with mutable objects
    content = copy.deepcopy(content)

    repo_param_fxt.add(content, backfill=True)
    print(repo_param_fxt)
    assert content == repo_param_fxt.get("/")


if __name__ == "__main__":
    pytest.main(["-vv"])
