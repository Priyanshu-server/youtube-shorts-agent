from dataclasses import dataclass
import os


@dataclass
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "default-service")
    env: str = os.getenv("ENV", "default")  # uppercase ENV for convention
    logger_name: str = "app_logger"


config = Settings()
