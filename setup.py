# -*- coding: utf-8 -*-
from setuptools import setup

# There is a problem with unicode characters in setup.cfg under Python 3.5 and 3.6
# See https://github.com/pypa/setuptools/issues/1062
# Try$ LC_ALL=C python3 setup.py --description
setup(author='Vlastimil Zíma')
