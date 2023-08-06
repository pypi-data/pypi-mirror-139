# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_ray', 'typed_ray.callbacks']

package_data = \
{'': ['*']}

install_requires = \
['mypy>=0.931,<0.932', 'ray>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'typed-ray',
    'version': '0.2.6',
    'description': 'Mypy plugin to add support for type checking ray objects.',
    'long_description': None,
    'author': 'Adi Gudimella',
    'author_email': 'aditya.gudimella@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
