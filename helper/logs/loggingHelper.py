import logging

from definitions import config
from helper.logs.coloredFormatter import ColoredFormatter


class LoggingHelper:
    @staticmethod
    def log_info(message, show_level: bool = True):
        LoggingHelper.get_logger(show_level=show_level).info(message)

    @staticmethod
    def log_debug(message):
        LoggingHelper.get_logger().debug(message)

    @staticmethod
    def log_warning(message):
        LoggingHelper.get_logger().warning(message)

    @staticmethod
    def log_error(message, show_level: bool = True):
        LoggingHelper.get_logger(show_level=show_level).error(message)

    @staticmethod
    def get_logger(name: str = config.LOGGER_NAME, show_level: bool = True):
        logger = logging.getLogger(name)
        if not show_level:
            logger = logging.getLogger(config.LOGGER_WITHOUT_LEVEL_NAME)

        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = ColoredFormatter('[%(levelname)s]: %(message)s') if show_level else (
                ColoredFormatter('%(message)s'))
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        return logger
