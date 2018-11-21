# -*- coding: utf-8 -*-
from setuptools import setup

EXTRAS_REQUIRE = {'quality': ['flake8', 'isort', 'pydocstyle'],
                  'tests': ['mock']}

setup(name='polint',
      version='0.2',
      description='Linter for gettext PO files',
      author='Vlastimil Zíma',
      author_email='vlastimil.zima@gmail.com',
      py_modules=['polint'],
      entry_points={'console_scripts': ['polint = polint:main']},
      install_requires=['polib'],
      extras_require=EXTRAS_REQUIRE,
      test_suite='tests')
