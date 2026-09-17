import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar

TRACE_ID_HEADER = "X-Trace-Id"

_trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def get_trace_id() -> str | None:
    return _trace_id_var.get()


def new_trace_id() -> str:
    return str(uuid.uuid4())


@contextmanager
def bind_trace_id(trace_id: str) -> Iterator[None]:
    token = _trace_id_var.set(trace_id)
    try:
        yield
    finally:
        _trace_id_var.reset(token)
