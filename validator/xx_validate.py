#!/usr/bin/env python
import os.path
import repackage
import argparse
import logging
import xxhash
repackage.up()
from validator.logging_output import logging_output
from validator.colors import bcolors


logger = logging.getLogger('xxHash_logger')


def run():
    parser = argparse.ArgumentParser(description="validate xxHash checksums (file: manifest-cache-xxh364.txt)")
    parser.add_argument('path')
    args = parser.parse_args()

    logging_output()
    path = args.path
    valid = True

    if not os.path.exists(path):
        logger.critical('Input path does not exist')
        exit(1)

    checksums = {}
    checksum_algo = 'xxHash3_64'

    with open(os.path.join(path, 'manifest-cache-xxh364.txt'), 'r') as content:
        for line in content:
            if line.startswith('#') or line.startswith('\n' or '\r'):
                continue

            checksum = line[0:20]
            checksum_path = line[20:].rstrip().lstrip(' \t').lstrip('*')

            if checksum and checksum_path:
                full_checksum_path = os.path.join(path, checksum_path)
                folder_filename = f'{checksum_path}' if len(path) == len(
                    path) else f'{path[len(path) + 1:]}/{checksum_path}'

                if os.path.isfile(full_checksum_path):
                    size = os.stat(full_checksum_path).st_size
                    checksums[folder_filename] = (checksum_algo, checksum, folder_filename, size)
                    actual_checksum = xxh3_64_with_chunk(full_checksum_path)

                    print(f'actual_checksum: {actual_checksum}\tchecksum: {checksum}')

                    if actual_checksum != checksum:
                        logger.error('Checksum missmatch: ' + checksum_path)
                        valid = False
                else:
                    logger.error('Checksum file not found: ' + checksum_path)
                    valid = False

    logger.info(str(len(checksum)) + ' files tested')
    if valid:
        logger.info(f'{bcolors.SUCCESS}Checksum test is valid! 👍')
    else:
        logger.error('Checksum test is not valid! 🙀')


def xxh3_64_with_chunk(filename):
    hash = xxhash.xxh3_64()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hash.update(chunk)
    return hash.intdigest()


if __name__ == '__main__':
    run()
