# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory', 'understory.cache', 'understory.cache.templates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'understory-cache',
    'version': '0.0.2',
    'description': 'Cache URLs and their contents',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
