#!/usr/bin/env python
from setuptools import setup

with open("README.rst") as fin:
    long_description = fin.read()

with open("loggingtofile/__init__.py") as fin:
    for line in fin:
        if line.startswith("__version__ ="):
            version = eval(line[14:])
            break

setup(name='loggingtofile',
      version=version,
      description='Write logging info to auto-created files.',
      author='Zhenyu ZHAO',
      author_email='mailtozyzhao@163.com',
      install_requires=[],
      long_description=long_description,
      url="https://github.com/Hideousmon/loggingtofile",
      packages=['loggingtofile']
      )