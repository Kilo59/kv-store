from starlette.status import HTTP_307_TEMPORARY_REDIRECT
from starlite import LoggingConfig, OpenAPIConfig, Provide, Starlite, delete, get
from starlite.controller import Controller
from starlite.datastructures import Redirect
from starlite.handlers import get, put

from kv_store import __version__
from kv_store.api.errors import ERROR_HANDLERS
from kv_store.api.repository import InMemoryRepository, Repository

logging_config = LoggingConfig(
    loggers={
        "my_app": {
            "level": "INFO",
            "handlers": ["queue_listener"],
        }
    }
)


@get(path="/health", include_in_schema=False)
def health_check() -> str:
    return "healthy"


@get(path="/", status_code=HTTP_307_TEMPORARY_REDIRECT, include_in_schema=False)
def docs_redirect() -> Redirect:
    """Redirect users to the reDoc page"""
    return Redirect(path="/schema")


Values = dict | list | str


class NameSpaceController(Controller):
    path = "/names"
    dependencies: dict[str, Provide] = {"repository": Provide(InMemoryRepository)}

    @get(description="Retrieve a list of all top-level namespaces")
    async def retrieve_root_namespaces(self, repository: Repository) -> list[str]:
        return list(repository.get("/").keys())

    @get(path="/{key:str}")
    async def get_item(self, key: str, repository: Repository) -> Values:
        return repository.get(key)

    @put(path="/{key:str}")
    async def set_item(self, key: str, data: Values, repository: Repository) -> Values:
        repository.add(data, key)
        return repository.get(key)

    @delete(path="/{key:str}")
    async def delete_item(self, key: str, repository: Repository) -> None:
        repository.delete(key)


app = Starlite(
    debug=True,  # non-prod only
    route_handlers=[health_check, docs_redirect, NameSpaceController],
    exception_handlers=ERROR_HANDLERS,
    on_startup=[logging_config.configure],
    openapi_config=OpenAPIConfig(title="KV Store", version=__version__),
)
