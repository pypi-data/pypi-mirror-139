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
    'version': '0.1.1',
    'description': 'Warn or fail on fixture name clash',
    'long_description': "# pytest-fixture-rtttg\n\n_In the face of ambiguity, refuse the temptation to guess._\n\nThis plugin detects when you have two fixtures that share the same name, and\nthrows an error in that case, instead of silently choosing the later/inner-most\none.\n\n\n## Installation\n\n    pip install pytest-fixture-rtttg\n\nAfter this, the plugin should automatically do its job.\n\n## Customization\n\nWhen the duplicate name is intentional, you can use the `dupe` mark to stop\nthis from happening:\n\n```py\n@pytest.fixture\n@pytest.mark.dupe\ndef some_fixture():\n    ...\n```\n\nUsually though, you're better of just choosing a different name.\n",
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/L3viathan/pytest-fixture-rtttg',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
