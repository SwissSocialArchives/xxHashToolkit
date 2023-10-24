import logging
import sys
from archiver.colors import bcolors
from archiver.definitions import get_config
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
    config = get_config()
    video_archival = logging.getLogger('video_archival')
    video_archival.setLevel(logging.INFO)
    video_archival_stdout_handler = logging.StreamHandler(sys.stdout)
    video_archival_stdout_handler.setLevel(level)
    video_archival_stdout_handler.setFormatter(VideoArchivalLoggingFormatter())

    video_archival_file_handler = logging.FileHandler(config['LOG']['dir'] + '/video-archival.log', encoding='utf8')
    video_archival_file_handler.setLevel(level)
    video_archival_file_handler.setFormatter(VideoArchivalLoggingFormatter())

    video_archival.addHandler(video_archival_stdout_handler)
    video_archival.addHandler(video_archival_file_handler)

    video_archival.newline = types.MethodType(log_newline, video_archival)

    bagit = logging.getLogger('bagit')
    bagit.setLevel(logging.WARNING)
    bagit_stdout_handler = logging.StreamHandler(sys.stdout)
    bagit_stdout_handler.setLevel(logging.WARNING)
    bagit_stdout_handler.setFormatter(CustomLoggingFormatter())

    bagit_file_handler = logging.FileHandler('bagit.log')
    bagit_file_handler.setLevel(logging.WARNING)
    bagit_file_handler.setFormatter(CustomLoggingFormatter())

    bagit.addHandler(bagit_stdout_handler)
    bagit.addHandler(bagit_file_handler)
