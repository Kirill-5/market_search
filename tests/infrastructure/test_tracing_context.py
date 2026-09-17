from src.infrastructure.tracing.context import TRACE_ID_HEADER


def test_trace_id_header_name() -> None:
    assert TRACE_ID_HEADER == "X-Trace-Id"
