# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlops_test']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.1,<2.0.0', 'requests>=2.20.1,<3.0.0']

setup_kwargs = {
    'name': 'mlops-test',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
