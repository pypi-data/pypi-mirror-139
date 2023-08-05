# -*- coding: UTF-8 -*-
"""
Setup
"""
import sys
import os
from setuptools import setup, find_packages

NAME = "longrun"

__version__ = "0.3a"
VERSION = __version__


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()


URL = "https://github.com/manbehindthemadness/longrun"
DESCRIPTION = "A simple utility allowing long running tasks to be executed without blocking"
LONG_DESCRIPTION = "See readme"

PACKAGES = find_packages()

if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported')

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords="async, asyncio, blocking",
    author="manbehindthemadness",
    url=URL,
    license="BSD",
    packages=PACKAGES,
    package_dir={'': 'src'},
    py_modules=['longrun']
)
