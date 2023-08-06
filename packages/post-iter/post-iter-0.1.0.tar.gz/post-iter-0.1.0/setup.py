# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['post_iter']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.12.0,<9.0.0', 'returns>=0.18.0,<0.19.0']

setup_kwargs = {
    'name': 'post-iter',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
