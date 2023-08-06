# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cse163_utils']

package_data = \
{'': ['*']}

install_requires = \
['descartes>=1.1.0,<2.0.0',
 'flake8>=4.0.1,<5.0.0',
 'geopandas>=0.10.2,<0.11.0',
 'matplotlib>=3.5.1,<4.0.0',
 'mock>=4.0.3,<5.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'scikit-image>=0.19.2,<0.20.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'cse163-utils',
    'version': '0.1.2',
    'description': 'Useful helper functions for CSE 163: Intermediate Data Programming course content. https://cse163.github.io/book/',
    'long_description': 'This package contains useful methods for CSE 163: Intermediate Data Programming.\n\nThe most commonly used functions for students will be\n\n```python\nfrom cse163_utils import download\n\ndownload("earthquakes.csv")\n```\n\nand\n\n```python\nfrom cse163_utils import assert_equals\n\nassert_equals(4, my_function("abc"))\n```\n\n\nFind out more:\n\n* Book: https://cse163.github.io/book/#\n* Course Website: cs.washington.edu/163\n* Source code: https://github.com/cse163/cse163_utils\n',
    'author': 'Hunter Schafer',
    'author_email': 'hschafer@cs.washington.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cse163.github.io/book/#',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
