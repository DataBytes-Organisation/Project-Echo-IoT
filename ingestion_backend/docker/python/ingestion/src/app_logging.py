"""
This module contains code relating to configuring logging for the application.
"""

import logging
import sys

LOG_FORMAT = "%(created)f:%(levelname)s:%(name)s:%(module)s:%(message)s"

class LogConfigurator:
    """
    This is a class with a single static method. Used to provide log configuration for
    the application.
    """
    @staticmethod
    def configure_logger(logger: logging.Logger) -> None:
        """
        Configurator pattern.  Takes in logger object and configures it.

        This method performs basic setup of:
            Outputs to stdout with a basic format.
            Sets logging level to INFO.
        Arguments:
            logger: logging.Logger
        Returns:
            None
        """
        handler: logging.Handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info("Logging configured.")
