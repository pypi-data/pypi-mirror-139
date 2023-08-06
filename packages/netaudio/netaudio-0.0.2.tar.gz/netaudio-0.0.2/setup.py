# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netaudio',
 'netaudio.console',
 'netaudio.console.commands',
 'netaudio.console.commands.channel',
 'netaudio.console.commands.config',
 'netaudio.console.commands.device',
 'netaudio.console.commands.subscription',
 'netaudio.dante',
 'netaudio.utils']

package_data = \
{'': ['*']}

install_requires = \
['cleo>=0.8.1,<0.9.0',
 'netifaces>=0.11.0,<0.12.0',
 'pyee>=9.0.4,<10.0.0',
 'twisted>=22.1.0,<23.0.0',
 'zeroconf>=0.38.3,<0.39.0']

entry_points = \
{'console_scripts': ['netaudio = netaudio:main']}

setup_kwargs = {
    'name': 'netaudio',
    'version': '0.0.2',
    'description': 'Control Dante network audio devices without Dante Controller',
    'long_description': None,
    'author': 'Christopher Ritsen',
    'author_email': 'chris.ritsen@gmail.com',
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
