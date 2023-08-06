# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpgtk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rpgtk',
    'version': '0.0.2.1a0',
    'description': 'the python rpg toolkit',
    'long_description': '# RPGTK :dice:',
    'author': 'Gabriel Sarmento',
    'author_email': 'gabrielfs.bot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/is-gabs/rpgtk',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
