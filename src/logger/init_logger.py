# Standard library
import logging
import os

# Third party library
import coloredlogs


def getLogger(logger_name: str):
    logger_name = os.path.basename(logger_name).replace(".py", "")
    logger = logging.getLogger(logger_name)
    coloredlogs.install(level="DEBUG", logger=logger)

    return logger
