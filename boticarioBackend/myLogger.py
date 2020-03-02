# Logger config for the whole project:
from colorlog import ColoredFormatter
import logging


def configureLogging(module_name=__name__):
    LOG_FORMAT = "%(log_color)s%(levelname)-8s %(module_log_color)s%(name)s  %(message_log_color)s%(message)s%(reset)s   %(time_log_color)s%(asctime)s"
    colored_formatter = ColoredFormatter(
        fmt=LOG_FORMAT,
        reset=True,
        datefmt='%H:%M:%S',
        log_colors={'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow',
                    'ERROR': 'red', 'CRITICAL': 'red,bg_white', },
        secondary_log_colors={
            'message': {'DEBUG': 'cyan', 'INFO': 'green', 'WARNING': 'yellow',
                        'ERROR': 'red,bold', 'CRITICAL': 'red,bg_white,bold', },
            'module': {'DEBUG': 'bold_blue', 'INFO': 'bold_blue', 'WARNING': 'bold_blue',
                       'ERROR': 'bold_red', 'CRITICAL': 'bold_red,bg_white', },
            'time': {'DEBUG': 'bold_white', 'INFO': 'bold_white', 'WARNING': 'bold_white',
                     'ERROR': 'bold_green', 'CRITICAL': 'bold_green', },
        }
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(colored_formatter)

    file_formatter = logging.Formatter(
        fmt="%(asctime)-8s %(levelname)-8s %(name)s -> %(message)s",
        datefmt='%d/%m (%H:%M:%S)'
    )
    file_handler = logging.FileHandler('./boticarioBackend/logs/error.log')
    file_handler.setLevel(logging.WARN)
    file_handler.setFormatter(file_formatter)

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
