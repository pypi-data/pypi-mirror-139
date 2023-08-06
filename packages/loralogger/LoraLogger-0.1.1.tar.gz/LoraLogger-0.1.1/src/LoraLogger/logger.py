# Contains a logger used by most LORA repos.

import logging

def logger(name, level):
    """
    Returns a custom logger.

    Args:
        name: (str): Name of the logger. Should always be '__name__'.
        level (str): The level of the logger
    Return:
        logging.logger(): Custom logger obj.
    """
    log_fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
    logging.basicConfig(level=level, format=log_fmt)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
