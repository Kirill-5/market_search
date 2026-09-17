import logging
import logging.config

from src.infrastructure.tracing.context import get_trace_id


class TraceIdLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = get_trace_id() or "-"
        return True


def configure_logging(level: int = logging.INFO) -> None:
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "trace_id": {"()": TraceIdLogFilter},
            },
            "formatters": {
                "default": {
                    "format": (
                        "%(asctime)s %(levelname)s [%(trace_id)s] %(name)s: %(message)s"
                    ),
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "filters": ["trace_id"],
                },
            },
            "root": {
                "level": level,
                "handlers": ["console"],
            },
        }
    )
