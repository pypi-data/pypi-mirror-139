# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visu3d']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'visu3d',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Conchylicultor',
    'author_email': 'etiennefg.pot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
