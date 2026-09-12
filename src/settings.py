import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = os.getenv(
        "POSTGRES_CONNECTION_STRING",
        os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5435/search_db",
        ),
    ).replace("postgres://", "postgresql+asyncpg://", 1)

    kafka_bootstrap_servers: str = os.getenv(
        "KAFKA_BROKERS", os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    )
    kafka_topic_ads: str = os.getenv(
        "KAFKA_TOPIC_MARKETPLACE_ADS", os.getenv("KAFKA_TOPIC_ADS", "ads")
    )
    kafka_consumer_group: str = os.getenv("KAFKA_CONSUMER_GROUP", "search-service")

    ad_service_url: str = os.getenv(
        "AD_SERVICE_URL",
        "http://student-kirill-5-marketplace-ad-service-web.student-kirill-5-marketplace-ad-service.svc.cluster.local:8000",
    )
