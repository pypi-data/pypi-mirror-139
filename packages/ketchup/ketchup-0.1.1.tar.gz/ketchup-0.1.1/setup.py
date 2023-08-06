# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ketchup']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'colorama>=0.4.4,<0.5.0',
 'termcolor>=1.1.0,<2.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ketchup = ketchup.cli:init']}

setup_kwargs = {
    'name': 'ketchup',
    'version': '0.1.1',
    'description': 'A (maybe) useful tool to launch your tests commands in parallel with style',
    'long_description': None,
    'author': 'Romain Commandé',
    'author_email': 'rcommande@meilleursagents.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rcommande/ketchup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
