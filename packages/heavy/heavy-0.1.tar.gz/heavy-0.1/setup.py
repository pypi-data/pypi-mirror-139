# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['heavy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'heavy',
    'version': '0.1',
    'description': 'Heavy',
    'long_description': '# Heavy\n\nStay tuned!\n',
    'author': 'HeavyAI',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
