# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vox_message']

package_data = \
{'': ['*']}

install_requires = \
['vox-django', 'vox-kafka']

setup_kwargs = {
    'name': 'vox-messages',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Jhonatan Teixeira',
    'author_email': 'jhonatan.teixeira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
