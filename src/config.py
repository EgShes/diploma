import os
from pathlib import Path

from src.logger import Logger


class PyCharmRemoteDebugError(Exception):
    pass


class EnvVariableNotDefinedError(Exception):
    pass


class DbConfig:
    db_service = "db"
    db_name = os.environ.get("POSTGRES_DB", None)
    db_user = os.environ.get("POSTGRES_USER", None)
    db_password = os.environ.get("POSTGRES_PASSWORD", None)

    @classmethod
    def get_db_url(cls):
        if cls.db_name is None or cls.db_user is None or cls.db_password is None:
            raise EnvVariableNotDefinedError(
                "Some of next envs not defined: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD"
            )
        return f"postgresql://{cls.db_user}:{cls.db_password}@{cls.db_service}/{cls.db_name}"


loggers_config_path = Path(__file__).parent / "loggers.conf"

app_logger = Logger.from_config("app_logger", loggers_config_path)
dev_logger = Logger.from_config("development_logger", loggers_config_path)
