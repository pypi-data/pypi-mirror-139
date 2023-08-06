# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymine_net',
 'pymine_net.net',
 'pymine_net.net.asyncio',
 'pymine_net.net.socket',
 'pymine_net.packets',
 'pymine_net.packets.v_1_18_1.handshaking',
 'pymine_net.packets.v_1_18_1.login',
 'pymine_net.packets.v_1_18_1.play',
 'pymine_net.packets.v_1_18_1.status',
 'pymine_net.types']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=36.0.1,<37.0.0', 'mutf8>=1.0.6,<2.0.0']

setup_kwargs = {
    'name': 'pymine-net',
    'version': '0.2.0',
    'description': 'Networking library for Minecraft in Python',
    'long_description': "# PyMine-Net\n[![CodeFactor](https://www.codefactor.io/repository/github/py-mine/pymine-net/badge)](https://www.codefactor.io/repository/github/py-mine/pymine-net)\n![code size](https://img.shields.io/github/languages/code-size/py-mine/PyMine-Net?color=0FAE6E)\n![code style](https://img.shields.io/badge/code%20style-black-000000.svg)\n\n*PyMine-Net - an extensible and modular Minecraft networking library in Python*\n\n## Features\n- Buffer class with methods for dealing with various types and data formats used by Minecraft\n- High level abstractions for packets with a system to seperate different protocol's packets\n- Miscellaneous classes for dealing with different Minecraft data structures relevant to networking\n",
    'author': 'PyMine-Net Developers & Contributors',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/py-mine/pymine-net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
