# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['medium_sdk_python',
 'medium_sdk_python.medium',
 'medium_sdk_python.tests',
 'notion2medium',
 'notion2medium.clients',
 'notion2medium.console',
 'notion2medium.console.commands',
 'notion2medium.exceptions']

package_data = \
{'': ['*']}

install_requires = \
['cleo==1.0.0a4',
 'notion-client>=0.9.0,<0.10.0',
 'notion2md>=2.7.1,<3.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['notion2medium = notion2medium.console.application:main']}

setup_kwargs = {
    'name': 'notion2medium',
    'version': '1.0.0',
    'description': 'a Simple command that publishes Notion Page to Medium.',
    'long_description': None,
    'author': 'echo724',
    'author_email': 'eunchan1001@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
