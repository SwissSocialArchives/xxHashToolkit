#!/usr/bin/env python
import os.path
import re
from datetime import datetime
import codecs

import repackage
import argparse
import xxhash

repackage.up()
from validator.logging import get_logger, get_SMTP_handler
from validator.definitions import get_config
from validator.colors import bcolors

config = get_config()
logger = get_logger('xx_hash_logger')


def run():

    parser = argparse.ArgumentParser(description="validate xxHash checksums (file: manifest-cache-xxh364.txt)")
    parser.add_argument('path')
    args = parser.parse_args()

    path = args.path
    valid = True

    if not os.path.exists(path):
        logger.critical('Input path does not exist')
        exit(1)

    tested_checksums = 0
    checksum_algo = 'xxHash3_64'
    datetime_now = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

    with open(os.path.join(path, 'manifest-cache-xxh364.txt'), 'r', encoding='utf-8') as content:
        for line in content:
            if line.startswith('#') or line.startswith('\n' or '\r'):
                continue

            pattern = re.compile(r'(\d+) +(.+)')
            checksum, checksum_path = pattern.split(line)[1:3]

            if checksum and checksum_path:
                full_checksum_path = os.path.join(path, checksum_path)

                if os.path.isfile(full_checksum_path):
                    size = os.stat(full_checksum_path).st_size
                    actual_checksum = xxh3_64_with_chunk(full_checksum_path)

                    if str(actual_checksum) != str(checksum):
                        logger.error('Checksum mismatch: ' + checksum_path)
                        valid = False
                    else:
                        tested_checksums += 1
                        logger.info(f'{datetime_now} ––– success: {checksum_path}')
                else:
                    logger.error(f'{datetime_now} ––– checksum path not found: {checksum_path}\n')
                    valid = False


    logger.info(f'{tested_checksums} files tested.')
    smtp_handler = get_SMTP_handler()
    logger.addHandler(smtp_handler)

    if valid:
        logger.info(f'{bcolors.SUCCESS}Checksum test was successful 👍')
    else:
        logger.error('Checksum test was not successful 🙀')


def xxh3_64_with_chunk(filename):
    hash = xxhash.xxh3_64()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hash.update(chunk)
    return hash.intdigest()

if __name__ == '__main__':
    run()
