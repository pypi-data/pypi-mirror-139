# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coshed_flask']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Compress>=1.10.1,<2.0.0',
 'Flask-Cors>=3.0.10,<4.0.0',
 'Flask-HTTPAuth>=4.5.0,<5.0.0',
 'Flask>=2.0.2,<3.0.0',
 'Werkzeug>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'coshed-flask',
    'version': '0.16.0',
    'description': 'flask helper for lazy developer(s)',
    'long_description': None,
    'author': 'doubleO8',
    'author_email': 'wb008@hdm-stuttgart.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
