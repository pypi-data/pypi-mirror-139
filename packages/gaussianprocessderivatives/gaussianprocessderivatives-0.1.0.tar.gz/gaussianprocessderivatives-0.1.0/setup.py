# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['gaussianprocessderivatives']
install_requires = \
['matplotlib>=3.5.1,<4.0.0', 'numpy>=1.22.2,<2.0.0', 'scipy>=1.8.0,<2.0.0']

setup_kwargs = {
    'name': 'gaussianprocessderivatives',
    'version': '0.1.0',
    'description': 'Uses Gaussian processes to smooth data and estimate first- and second-order derivatives',
    'long_description': None,
    'author': 'Peter Swain',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
