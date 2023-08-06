# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvdastwrapper']

package_data = \
{'': ['*'],
 'cvdastwrapper': ['templates/*',
                   'templates/assets/images/*',
                   'templates/assets/images/charts/*',
                   'templates/assets/styles/*']}

install_requires = \
['cvdast']

entry_points = \
{'console_scripts': ['cvdast-wrapper = cvdastwrapper.entry:main']}

setup_kwargs = {
    'name': 'cvdastwrapper',
    'version': '1.48.21',
    'description': 'This is a wrapper around CVDAST',
    'long_description': open('README.rst').read(),
    'author': 'Bala Kumaran',
    'author_email': 'balak@cloudvector.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
