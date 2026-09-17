import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_trace_id_echoed_from_request_header(client: AsyncClient) -> None:
    resp = await client.get("/search", headers={"X-Trace-Id": "demo-123"})

    assert resp.headers["X-Trace-Id"] == "demo-123"


@pytest.mark.asyncio
async def test_trace_id_generated_when_missing(client: AsyncClient) -> None:
    resp = await client.get("/search")

    generated = resp.headers["X-Trace-Id"]
    assert uuid.UUID(generated)
