# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chanjo2', 'chanjo2.endpoints', 'chanjo2.meta', 'chanjo2.models']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.68.1,<0.69.0',
 'pyd4>=0.1.13,<0.2.0',
 'sqlmodel>=0.0.4,<0.0.5',
 'uvicorn>=0.15.0,<0.16.0']

setup_kwargs = {
    'name': 'chanjo2',
    'version': '0.1.0',
    'description': 'Next generation coverage analysis',
    'long_description': None,
    'author': 'moonso',
    'author_email': 'mans.magnusson@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
