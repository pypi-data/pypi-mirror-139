# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chispa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chispa',
    'version': '0.9.0',
    'description': 'Pyspark test helper library',
    'long_description': None,
    'author': 'MrPowers',
    'author_email': 'matthewkevinpowers@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
