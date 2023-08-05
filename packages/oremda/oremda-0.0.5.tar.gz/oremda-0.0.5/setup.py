# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oremda', 'oremda.meta']

package_data = \
{'': ['*']}

install_requires = \
['oremda-cli>=0.0.2,<0.0.3',
 'oremda-client>=0.0.2,<0.0.3',
 'oremda-core>=0.0.2,<0.0.3',
 'oremda-engine>=0.0.4,<0.0.5',
 'oremda-server>=0.0.2,<0.0.3']

entry_points = \
{'oremda.cli.plugin': ['start = oremda.meta.cli:main']}

setup_kwargs = {
    'name': 'oremda',
    'version': '0.0.5',
    'description': '',
    'long_description': '',
    'author': 'Alessandro Genova',
    'author_email': 'alessandro.genova@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
