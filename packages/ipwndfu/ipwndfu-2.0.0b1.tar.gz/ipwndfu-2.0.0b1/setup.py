# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ipwndfu', 'libusbfinder', 'usb', 'usb.backend']

package_data = \
{'': ['*'], 'ipwndfu': ['bin/*'], 'libusbfinder': ['bottles/*']}

install_requires = \
['cryptography>=36.0.1,<37.0.0']

entry_points = \
{'console_scripts': ['ipwndfu = ipwndfu.main:main']}

setup_kwargs = {
    'name': 'ipwndfu',
    'version': '2.0.0b1',
    'description': 'The DFU exploitation toolkit for Apple devices',
    'long_description': None,
    'author': 'axi0mX',
    'author_email': 'axi0mXor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
