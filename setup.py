#!/usr/bin/env python3

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='xxHashTool',
      version='1.0',
      description='xxhash toolkit for swiss social archives',
      url='',
      authors='Fabian Würtz, Stefan Fuhlroth',
      license='',
      packages=find_packages("validator"),
      package_dir={"": "validator"},
      entry_points={
          "console_scripts": [
              "validate = validate:run",
          ],
      },
      python_requires='>3.5.2',
      install_requires=[
        'repackage', 'xxhash'
      ])
