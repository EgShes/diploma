import os


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


class Config:
    remote_debug_enabled = os.environ.get("REMOTE_DEBUG", 0) == "1"


if Config.remote_debug_enabled:
    import pydevd_pycharm

    try:
        pydevd_pycharm.settrace("172.17.0.1", port=12345, stdoutToServer=True, stderrToServer=True)
    except ConnectionRefusedError as e:
        raise PyCharmRemoteDebugError("Could not connect to remote server") from e
