# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slrzd']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'slrzd',
    'version': '0.0.1',
    'description': 'Solarize everything',
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
