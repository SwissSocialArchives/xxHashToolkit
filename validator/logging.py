import os
import sys
import logging
import logging.handlers

from validator.colors import bcolors
from validator.definitions import get_config
import types

import __main__
from datetime import datetime


config = get_config()


class CustomLoggingFormatter(logging.Formatter):
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)-8s - %(message)s (%(funcName)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: format + reset,
        logging.WARNING: bcolors.WARNING + format + reset,
        logging.ERROR: bcolors.ERROR + format + reset,
        logging.CRITICAL: bcolors.CRITICAL + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)


def get_filehandler():
    dest_folder = os.path.basename(os.path.normpath(__main__.sys.argv[1]))
    script = os.path.basename(os.path.normpath(__main__.__file__))
    datetime_now = datetime.now().strftime("%Y:%m:%d--%H-%M-%S")

    return logging.FileHandler(config['LOG']['dir'] + f'/{dest_folder}_{datetime_now}__{script}.log',
                               encoding='utf8')


def get_SMTP_handler():
    mailhost = (config['MAIL']['host'], config['MAIL']['port'])
    fromaddr = config['MAIL']['sender']
    toaddr = config['MAIL']['receivers']
    subject = 'xx_validate'
    credentials = (config['MAIL']['sender'], config['MAIL']['password'])

    return logging.handlers.SMTPHandler(mailhost, fromaddr, toaddr, subject, credentials)


def log_newline(self):
    print('')


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = get_filehandler()

    for handler in [stdout_handler, file_handler]:

        stdout_handler.setLevel(level)
        stdout_handler.setFormatter(CustomLoggingFormatter())
        logger.addHandler(handler)

    logger.newline = types.MethodType(log_newline, logger)
    return logger
