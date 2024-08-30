import logging

from definitions import config
from helper.logs.coloredFormatter import ColoredFormatter


class LoggingHelper:
    @staticmethod
    def log_info(message):
        LoggingHelper.get_logger().info(message)

    @staticmethod
    def log_debug(message):
        LoggingHelper.get_logger().debug(message)

    @staticmethod
    def log_warning(message):
        LoggingHelper.get_logger().warning(message)

    @staticmethod
    def log_error(message):
        LoggingHelper.get_logger().error(message)

    @staticmethod
    def get_logger(name: str = config.LOGGER_NAME):
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = ColoredFormatter('[%(levelname)s]: %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        return logger
