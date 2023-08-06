# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['diffword']
install_requires = \
['click>=8.0.3,<9.0.0',
 'python-docx-docm>=0.1.0,<0.2.0',
 'regex>=2022.1.18,<2023.0.0']

entry_points = \
{'console_scripts': ['diffword = diffword:main']}

setup_kwargs = {
    'name': 'diffword',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ajanvrin',
    'author_email': 'alexandre.janvrin@reseau.eseo.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
