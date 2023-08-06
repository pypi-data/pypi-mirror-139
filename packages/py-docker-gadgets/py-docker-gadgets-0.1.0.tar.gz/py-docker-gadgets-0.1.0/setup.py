# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_gadgets']

package_data = \
{'': ['*']}

install_requires = \
['docker>=5.0.3,<6.0.0', 'loguru>=0.6.0,<0.7.0', 'py-buzz>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'py-docker-gadgets',
    'version': '0.1.0',
    'description': 'Some convenience tools for managing docker containers in python',
    'long_description': None,
    'author': 'Tucker Beck',
    'author_email': 'tucker.beck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
