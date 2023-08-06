# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_fixture_rtttg']
install_requires = \
['pytest>=7.0.1,<8.0.0']

entry_points = \
{'pytest11': ['fixture_rtttg = pytest_fixture_rtttg']}

setup_kwargs = {
    'name': 'pytest-fixture-rtttg',
    'version': '0.1.0',
    'description': 'Warn or fail on fixture name clash',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
