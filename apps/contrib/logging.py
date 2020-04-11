import logging


class Logger(object):

    logger = None

    def __init__(self):
        self.logs = logging.getLogger(__name__)

    @classmethod
    def debug(cls, message):
        cls().logs.debug(message)

    @classmethod
    def info(cls, message):
        cls().logs.info(message)

    @classmethod
    def error(cls, message):
        cls().logs.error(message)

    @classmethod
    def warning(cls, message):
        cls().logs.warning(message)
