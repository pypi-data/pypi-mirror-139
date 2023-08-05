# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['equanpy']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['equanpy = equanpy.main:cli']}

setup_kwargs = {
    'name': 'equanpy',
    'version': '1.0.0',
    'description': 'Python packaging data school',
    'long_description': None,
    'author': 'Didier SCHMITT',
    'author_email': 'dschmitt@equancy.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
