# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fentoboardimage']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0']

setup_kwargs = {
    'name': 'fentoboardimage',
    'version': '1.0.0',
    'description': 'FenToBoardImage takes a Fen string representing a Chess position, and renders a Pillow image of the resulting position.',
    'long_description': None,
    'author': 'Reed Krawiec',
    'author_email': 'reedkrawiec@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
