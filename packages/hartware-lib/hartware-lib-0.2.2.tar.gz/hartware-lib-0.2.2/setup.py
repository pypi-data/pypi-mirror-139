# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hartware_lib',
 'hartware_lib.adapters',
 'hartware_lib.commands',
 'hartware_lib.core',
 'hartware_lib.core.settings',
 'hartware_lib.exceptions',
 'hartware_lib.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'slack-sdk>=3.11.2,<4.0.0']

entry_points = \
{'console_scripts': ['slack_send = hartware_lib.commands.slack:main']}

setup_kwargs = {
    'name': 'hartware-lib',
    'version': '0.2.2',
    'description': 'Core helper lib for Hartware codes.',
    'long_description': '# Hartware Lib\n',
    'author': 'Laurent Arthur',
    'author_email': 'laurent.arthur75@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ludwig778/python-lib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
