from pathlib import Path
import configparser
import argparse
import os.path


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def get_config():
    config = configparser.ConfigParser(allow_no_value=True)
    config_file_name = str(get_project_root()) + '/config.ini'
    if os.path.isfile(config_file_name):
        config.read(config_file_name)
        return config

    config_file_name = str(get_project_root()) + '/config.example.ini'
    if os.path.isfile(config_file_name):
        config.read(config_file_name)
        return config

