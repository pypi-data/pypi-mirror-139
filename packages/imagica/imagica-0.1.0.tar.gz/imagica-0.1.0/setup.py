# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imagica']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0', 'opencv-python>=4.5.5,<5.0.0']

setup_kwargs = {
    'name': 'imagica',
    'version': '0.1.0',
    'description': 'A package to help with image processing',
    'long_description': '# imagica\nA package to help with image processing for Python\n',
    'author': 'MagicalLiebe',
    'author_email': 'magical.liebe@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MagicalLiebe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
