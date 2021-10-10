import os


class PyCharmRemoteDebugError(Exception):
    pass


class DbConfig:
    db_service = "db"
    db_name = os.environ.get("DB_NAME", "")
    db_user = os.environ.get("DB_USER", "")
    db_password = os.environ.get("DB_PASSWORD", "")

    @classmethod
    def get_db_url(cls):
        return f"postgresql://{cls.db_user}:{cls.db_password}@{cls.db_service}/{cls.db_name}"


class Config:
    remote_debug_enabled = os.environ.get("REMOTE_DEBUG", 0) == "1"


if Config.remote_debug_enabled:
    import pydevd_pycharm

    try:
        pydevd_pycharm.settrace(
            "172.17.0.1", port=12345, stdoutToServer=True, stderrToServer=True
        )
    except ConnectionRefusedError as e:
        raise PyCharmRemoteDebugError("Could not connect to remote server") from e
