"""
Error handling
"""
import logging

import glom_dict as gd
from starlette.status import HTTP_404_NOT_FOUND
from starlite import MediaType, Request, Response

LOGGER = logging.getLogger(__file__)


def path_access_error_handler(_: Request, exc: gd.PathAccessError) -> Response:
    LOGGER.info(exc.path)
    return Response(
        media_type=MediaType.JSON,
        content={
            "message": exc.get_message(),
            "details": {
                "part": exc.part_idx,
                "path": exc.path.values(),
            },
            "status_code": HTTP_404_NOT_FOUND,
        },
        status_code=HTTP_404_NOT_FOUND,
    )


ERROR_HANDLERS = {gd.PathAccessError: path_access_error_handler}
