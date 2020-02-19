import logging
from logging.config import dictConfig

def create_logger(config_dict, default_logger='api'):
    """Get the api logger and define its configuration
    The default logger name is 'api'
    """

    logging.config.dictConfig(config_dict)

    logger = logging.getLogger(default_logger)

    return logger
