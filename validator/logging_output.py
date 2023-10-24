import logging
import sys
from validator.colors import bcolors
import types


class CustomLoggingFormatter(logging.Formatter):
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: format + reset,
        logging.WARNING: bcolors.WARNING + format + reset,
        logging.ERROR: bcolors.ERROR + format + reset,
        logging.CRITICAL: bcolors.CRITICAL + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class VideoArchivalLoggingFormatter(logging.Formatter):
    reset = "\x1b[0m"
    format = "{asctime:2s} {levelname:^8s} {message:s}"
    FORMATS = {
        logging.DEBUG: format + reset,
        logging.INFO: format + reset,
        logging.WARNING: bcolors.WARNING + format + reset,
        logging.ERROR: bcolors.ERROR + format + reset,
        logging.CRITICAL: bcolors.CRITICAL + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S', style='{')
        return formatter.format(record)


def log_newline(self):
    print('')


def logging_output(level=logging.INFO):
    xxHash = logging.getLogger('xxHash-logger')
    xxHash.setLevel(logging.INFO)
    xxHash_stdout_handler = logging.StreamHandler(sys.stdout)
    xxHash_stdout_handler.setLevel(level)
    xxHash_stdout_handler.setFormatter(VideoArchivalLoggingFormatter())

    xxHash_file_handler = logging.FileHandler('video-archival.log', encoding='utf8')
    xxHash_file_handler.setLevel(level)
    xxHash_file_handler.setFormatter(VideoArchivalLoggingFormatter())

    xxHash.addHandler(xxHash_stdout_handler)
    xxHash.addHandler(xxHash_file_handler)

    xxHash.newline = types.MethodType(log_newline, xxHash)

    core = logging.getLogger('core-logging')
    core.setLevel(logging.WARNING)
    core_stdout_handler = logging.StreamHandler(sys.stdout)
    core_stdout_handler.setLevel(logging.WARNING)
    core_stdout_handler.setFormatter(CustomLoggingFormatter())

    core_file_handler = logging.FileHandler('core.log')
    core_file_handler.setLevel(logging.WARNING)
    core_file_handler.setFormatter(CustomLoggingFormatter())

    core.addHandler(core_stdout_handler)
    core.addHandler(core_file_handler)
