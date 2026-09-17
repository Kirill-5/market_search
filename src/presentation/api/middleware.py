from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response

from src.infrastructure.tracing.context import (
    TRACE_ID_HEADER,
    bind_trace_id,
    new_trace_id,
)


async def trace_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    trace_id = request.headers.get(TRACE_ID_HEADER) or new_trace_id()
    with bind_trace_id(trace_id):
        response = await call_next(request)
    response.headers[TRACE_ID_HEADER] = trace_id
    return response


def install_tracing_middleware(app: FastAPI) -> None:
    app.middleware("http")(trace_id_middleware)
