import logging.config
from pathlib import Path
from typing import Union

import yaml


class Logger:
    @classmethod
    def from_config(cls, logger_name: str, config_path: Union[str, Path]) -> logging.Logger:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f.read())
        assert (
            logger_name in config["loggers"]
        ), f"No config found for the {logger_name} logger. Expected names {config['loggers']}"
        config["disable_existing_loggers"] = False
        logging.config.dictConfig(config)
        return logging.getLogger(logger_name)
