# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pactsdk']

package_data = \
{'': ['*']}

install_requires = \
['py-algorand-sdk>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'pactsdk',
    'version': '0.1.0',
    'description': 'Python SDK for Pact smart contracts',
    'long_description': None,
    'author': 'Mateusz Tomczyk',
    'author_email': 'mateusz@ulam.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
