import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass, field
from typing import Any

from src.application.services.kafka_ads_consumer import KafkaAdsConsumer
from src.application.usecases.index_ad import IndexAd
from src.application.usecases.remove_ad import RemoveAd
from tests.conftest import FakeAdSource, FakeUnitOfWork, make_snapshot


@dataclass
class FakeKafkaMessage:
    value: dict[str, Any]
    headers: list[tuple[str, bytes]] = field(default_factory=list)


class FakeAIOKafkaConsumer:
    def __init__(self, messages: list[FakeKafkaMessage]) -> None:
        self._messages = messages
        self.commits = 0

    def __aiter__(self) -> AsyncIterator[FakeKafkaMessage]:
        return self._iterate()

    async def _iterate(self) -> AsyncIterator[FakeKafkaMessage]:
        for message in self._messages:
            yield message

    async def commit(self) -> None:
        self.commits += 1


async def test_trace_id_from_kafka_headers_reaches_ad_source(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=1))
    consumer = FakeAIOKafkaConsumer(
        [
            FakeKafkaMessage(
                value={"event": "ad.created", "payload": {"ad_id": 1}},
                headers=[("X-Trace-Id", b"demo-123")],
            )
        ]
    )
    ads_consumer = KafkaAdsConsumer(
        consumer=consumer,  # type: ignore[arg-type]
        index_ad=IndexAd(fake_uow, fake_ad_source),
        remove_ad=RemoveAd(fake_uow),
    )

    await ads_consumer.run()

    assert fake_ad_source.trace_ids_seen == ["demo-123"]
    assert consumer.commits == 1


async def test_missing_headers_generates_trace_id(
    fake_uow: FakeUnitOfWork,
    fake_ad_source: FakeAdSource,
) -> None:
    fake_ad_source.set(make_snapshot(ad_id=1))
    consumer = FakeAIOKafkaConsumer(
        [FakeKafkaMessage(value={"event": "ad.created", "payload": {"ad_id": 1}})]
    )
    ads_consumer = KafkaAdsConsumer(
        consumer=consumer,  # type: ignore[arg-type]
        index_ad=IndexAd(fake_uow, fake_ad_source),
        remove_ad=RemoveAd(fake_uow),
    )

    await ads_consumer.run()

    assert len(fake_ad_source.trace_ids_seen) == 1
    generated = fake_ad_source.trace_ids_seen[0]
    assert generated is not None
    assert uuid.UUID(generated)
