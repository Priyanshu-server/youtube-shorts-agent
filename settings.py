from dataclasses import dataclass, field, fields
import os

from src.utils.logging import configure_logging, get_logger


@dataclass
class Settings:
    service_name: str = field(default_factory=lambda: os.getenv("SERVICE_NAME", "youtube-shorts-agent"))
    env: str = field(default_factory=lambda: os.getenv("ENV", "development"))
    logger_name: str = "app_logger"
    open_ai_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", None))

    def __post_init__(self):
        configure_logging()
        self._log()

    def _log(self):
        logger = get_logger(self.logger_name, service=self.service_name, env=self.env)
        status = {f.name: bool(getattr(self, f.name)) for f in fields(self)}
        logger.info("Settings loaded", extra=status)


config = Settings()
