# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_diff_selector']

package_data = \
{'': ['*']}

install_requires = \
['pyan3>=1.2.0,<2.0.0', 'tqdm>=4.62.3,<5.0.0', 'unidiff>=0.7.3,<0.8.0']

entry_points = \
{'console_scripts': ['selector = pytest_diff_selector.main:run'],
 'pytest11': ['pytest-diff-selector = pytest_diff_selector.plugin']}

setup_kwargs = {
    'name': 'pytest-diff-selector',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pytest-diff-selector',
    'author': 'Israel Fruchter',
    'author_email': 'israel.fruchter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fruch/pytest-diff-selector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
