# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_logging_context']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-logging-context',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Christian Hartung',
    'author_email': 'hartung@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
