import os


class Config:
    remote_debug_enabled = os.environ.get("REMOTE_DEBUG", 0) == "1"


if Config.remote_debug_enabled:
    import pydevd_pycharm

    pydevd_pycharm.settrace(
        "172.17.0.1", port=12345, stdoutToServer=True, stderrToServer=True
    )
