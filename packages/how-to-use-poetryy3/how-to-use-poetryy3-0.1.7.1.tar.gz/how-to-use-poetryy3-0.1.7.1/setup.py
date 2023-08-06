# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['how_to_use_poetryy3']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.1.0,<23.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'how-to-use-poetryy3',
    'version': '0.1.7.1',
    'description': '',
    'long_description': None,
    'author': 'ramazangur',
    'author_email': 'ramazangur@zoho.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
