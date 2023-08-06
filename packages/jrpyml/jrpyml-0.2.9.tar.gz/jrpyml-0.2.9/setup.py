# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrpyml', 'jrpyml.datasets']

package_data = \
{'': ['*'], 'jrpyml.datasets': ['data/*']}

install_requires = \
['graphviz>=0.10,<0.11',
 'matplotlib>=3.1,<4.0',
 'numpy>=1.22,<2.0',
 'pandas>=1,<2',
 'scikit-learn>=1,<2',
 'scipy>=1.2,<2.0',
 'seaborn>=0.11,<0.12',
 'statsmodels>=0,<1']

setup_kwargs = {
    'name': 'jrpyml',
    'version': '0.2.9',
    'description': 'Jumping Rivers: Machine Learning with Python',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
