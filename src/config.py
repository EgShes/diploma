import os
from pathlib import Path

from src.logger import Logger


class PyCharmRemoteDebugError(Exception):
    pass


class EnvVariableNotDefinedError(Exception):
    pass


class DbConfig:
    db_service = os.environ.get("POSTGRES_HOST", "db")
    db_port = os.environ.get("POSTGRES_PORT", 5432)
    db_name = os.environ.get("POSTGRES_DB", None)
    db_user = os.environ.get("POSTGRES_USER", None)
    db_password = os.environ.get("POSTGRES_PASSWORD", None)

    @classmethod
    def get_db_url(cls):
        if cls.db_name is None or cls.db_user is None or cls.db_password is None:
            raise EnvVariableNotDefinedError(
                "Some of next envs not defined: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD"
            )
        return f"postgresql://{cls.db_user}:{cls.db_password}@{cls.db_service}:{cls.db_port}/{cls.db_name}"


class RabbitConfig:
    url = os.environ.get("RABBIT_URL")


class DispatcherConfig:
    words_batch = 5
    words_sleep = 5
    named_entities_batch = 5
    named_entities_sleep = 5
    sentiments_batch = 5
    sentiments_sleep = 5


loggers_config_path = Path(__file__).parent / "loggers.conf"

app_logger = Logger.from_config("app_logger", loggers_config_path)
ner_logger = Logger.from_config("ner_logger", loggers_config_path)
words_logger = Logger.from_config("words_logger", loggers_config_path)
dev_logger = Logger.from_config("development_logger", loggers_config_path)
