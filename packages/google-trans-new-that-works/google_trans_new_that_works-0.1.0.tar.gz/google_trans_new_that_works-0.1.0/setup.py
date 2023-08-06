# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_trans_new_that_works']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0', 'urllib3>=1.26.8,<2.0.0']

setup_kwargs = {
    'name': 'google-trans-new-that-works',
    'version': '0.1.0',
    'description': 'Google translate that works ( i think )',
    'long_description': None,
    'author': 'Sayan Biswas',
    'author_email': 'sayan@intellivoid.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
