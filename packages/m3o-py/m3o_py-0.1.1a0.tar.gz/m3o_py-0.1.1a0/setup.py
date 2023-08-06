# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['m3o_py']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0', 'aiohttp>=3.8.1,<4.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'm3o-py',
    'version': '0.1.1a0',
    'description': '',
    'long_description': None,
    'author': 'Mawoka',
    'author_email': 'mawoka-myblock@e.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
