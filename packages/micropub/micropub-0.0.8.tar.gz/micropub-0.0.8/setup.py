# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['micropub']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['micropub = micropub.__main__:main']}

setup_kwargs = {
    'name': 'micropub',
    'version': '0.0.8',
    'description': 'Micropub client',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@ragt.ag',
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
