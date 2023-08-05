# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaad']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yaad',
    'version': '0.1.0',
    'description': 'Yet Another Attribute Dict',
    'long_description': '',
    'author': 'Daniel Sullivan',
    'author_email': 'mumblepins@users.noreply.github.com ',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mumblepins/yaad',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
