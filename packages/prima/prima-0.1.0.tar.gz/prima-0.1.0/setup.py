# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prima',
 'prima.configuration',
 'prima.configuration.utils',
 'prima.engine',
 'prima.utils']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.4,<0.4.0',
 'fn>=0.4.3,<0.5.0',
 'funcy>=1.17,<2.0',
 'matplotlib>=3.5.1,<4.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'parameterized>=0.8.1,<0.9.0',
 'pathos>=0.2.8,<0.3.0',
 'plotly>=5.6.0,<6.0.0',
 'pytest>=7.0.1,<8.0.0',
 'pytz>=2021.3,<2022.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0',
 'six>=1.16.0,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'wheel>=0.37.1,<0.38.0',
 'xarray>=0.21.1,<0.22.0']

setup_kwargs = {
    'name': 'prima',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kivo360',
    'author_email': 'kivo360@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
